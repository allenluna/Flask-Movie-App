from flask import Blueprint, request, redirect, render_template, flash, url_for, jsonify
from flask_login import current_user
from .model import Movies, Cast, Popular, Upcomming
from . import db
import requests
import os

post_movie = Blueprint("post_movie", __name__)

MOVIE_KEY = os.environ.get("MOVIE_KEY")
SEARCH_URL = os.environ.get("SEARCH_URL")
MOVIE_VIDEO = os.environ.get("MOVIE_VIDEO")
MOVIE_URL = os.environ.get("MOVIE_URL")

BANNER_IMAGE = os.environ.get("BANNER_IMAGE")
IMG_URL = os.environ.get("IMG_URL")
CAST_IMG = os.environ.get("CAST_IMG")
CREDITS_URL = os.environ.get("CREDITS_URL")
POSTER_URL = os.environ.get("POSTER_URL")
YOUTUBE_EMBED =os.environ.get("YOUTUBE_EMBED")
REVIEWS_URL = os.environ.get("REVIEWS_URL")

HEADER = {
        "accept": "application/json",
        "Authorization" : f"Bearer {MOVIE_KEY}"
}

@post_movie.route("/upload-movie")
def upload_movie():
    id = request.args.get("id")
    if id:
        url_movie = f"{MOVIE_VIDEO}{id}/videos"
        url_data = f"{MOVIE_URL}{id}"
        get_image = f"{POSTER_URL}{id}/images"
        cast_url = f"{CREDITS_URL}{id}/credits"
        review_url = f"{REVIEWS_URL}{id}/reviews"

        
        # trailer data
        video_response = requests.get(url_movie, params={"language": "en-US"}, headers=HEADER)
        video_data = video_response.json()["results"]
        movie_response = requests.get(url_data, headers=HEADER, params={"language": "en-US"})
        movie_data = movie_response.json()


        # cast data
        cast_response = requests.get(cast_url, headers=HEADER)
        cast_data = cast_response.json()["cast"]
        

        # Image data
        banner = requests.get(get_image, headers=HEADER)
        banner_data = banner.json()["backdrops"][0]["file_path"]
        image = requests.get(get_image, headers=HEADER)
        image_data = image.json()["posters"][0]["file_path"]


        if len(video_data) == 0:
            flash("No movie file.")
            return redirect(request.referrer)
        
        
        characters = [Cast(cast_id=movie_data["id"], name=cast_charac["name"], cast_img=f'{CAST_IMG}{cast_charac["profile_path"]}') for cast_charac in cast_data]

        if Movies.query.filter(Movies.id == movie_data["id"]).all():
            flash("Movie is already in a lists.")
            return redirect(url_for("post_movie.movie"))
        new_movie = Movies(
            id = movie_data["id"],
            title = movie_data["title"],
            overview = movie_data["overview"],
            banner = f'{BANNER_IMAGE}{banner_data}',
            image = f'{IMG_URL}{image_data}',
            movie = f'{YOUTUBE_EMBED}{video_data[0]["key"]}',
            key = video_data[0]["key"],
            date = movie_data["release_date"],
            user_name = current_user
        )        

        db.session.add(new_movie)
        db.session.add_all(characters)
        db.session.commit()
        return redirect(url_for("post_movie.movie"))
    

    
@post_movie.route("/post-movie", methods=["GET", "POST"])
def movie():
    
    if request.method == "POST":
        param = {
            "query" : request.form.get("title")
        }
        response = requests.get(SEARCH_URL, params=param, headers=HEADER)
        datas = response.json()["results"]
        return render_template("savemovie.html", datas=datas, img_display=IMG_URL)
                
    return render_template("post_movies.html")

@post_movie.route("/popular")
def popular():
    popular_url = "https://api.themoviedb.org/3/movie/popular"

    # popular data
    response = requests.get(popular_url, headers=HEADER)
    datas = response.json()["results"]

    # image data from popular data
    list_image = [f"https://api.themoviedb.org/3/movie/{data['id']}/images" for data in datas]
    list_image_data = [f"{IMG_URL}{requests.get(list_image[image], headers=HEADER).json()['posters'][0]['file_path']}" for image in range(len(list_image))]
    list_banner = [f"https://api.themoviedb.org/3/movie/{data['id']}/images" for data in datas]
    list_banner_data = [f"{BANNER_IMAGE}{requests.get(list_banner[image], headers=HEADER).json()['backdrops'][0]['file_path']}" for image in range(len(list_image))]

    # fetch video and movie data from popular
    list_movie = [f"{MOVIE_VIDEO}{data['id']}/videos" for data in datas]
    list_movie_data = [
        f"{YOUTUBE_EMBED}{requests.get(list_movie[video], params={'language': 'en-US'}, headers=HEADER).json()['results'][0]['key']}"
        for video in range(len(list_movie))
    ]
    key = [requests.get(list_movie[video], params={'language': 'en-US'}, headers=HEADER).json()['results'][0]['key'] for video in range(len(list_movie))]
    
    movie_data = [requests.get(f"{MOVIE_URL}{data['id']}", headers=HEADER).json() for data in datas]
        
    lists_cast = [requests.get(f"{CREDITS_URL}{data['id']}/credits", headers=HEADER).json()["cast"] for data in datas]
    characters = [Cast(cast_id=movie_data[_]["id"], name=lists_cast[_][cast]["name"], cast_img=f'{CAST_IMG}{lists_cast[_][cast]["profile_path"]}') for _ in range(len(lists_cast)) for cast in range(len(lists_cast[_]))]
    
    
    if Popular.query.filter(Popular.id).count() == 0:
        popular_movies = [
            Popular(
            id=movie_data[data]["id"],
            title=movie_data[data]["title"],
            overview=movie_data[data]["overview"],
            banner = list_banner_data[data],
            image = list_image_data[data],
            movie = list_movie_data[data],
            key = key[data],
            date=movie_data[data]["release_date"]
            )  
            for data in range(len(datas))
            ]
        db.session.add_all(popular_movies)
        db.session.add_all(characters)
        db.session.commit()
        return redirect(url_for("view.popular_data"))
    
    return redirect(url_for("view.popular_data"))

@post_movie.route("/upcomming", methods=["GET", "POST"])
def upcomming():
    upcomming_url = "https://api.themoviedb.org/3/movie/upcoming"

    response = requests.get(upcomming_url, headers=HEADER)
    datas = response.json()["results"]
    

     # image data from popular data
    list_image = [f"https://api.themoviedb.org/3/movie/{data['id']}/images" for data in datas]
    list_image_data = [f"{IMG_URL}{requests.get(list_image[image], headers=HEADER).json()['posters'][0]['file_path']}" for image in range(len(list_image))]
    list_banner = [f"https://api.themoviedb.org/3/movie/{data['id']}/images" for data in datas]
    list_banner_data = [f"{BANNER_IMAGE}{requests.get(list_banner[image], headers=HEADER).json()['backdrops'][0]['file_path']}" for image in range(len(list_image))]

    # fetch video and movie data from popular
    list_movie = [f"{MOVIE_VIDEO}{data['id']}/videos" for data in datas]

    list_movie_data = [
        f"{YOUTUBE_EMBED}{requests.get(list_movie[video], params={'language': 'en-US'}, headers=HEADER).json()['results'][0]['key']}"
        for video in range(len(list_movie) - 1)
    ]
    
    key = [requests.get(list_movie[video], params={'language': 'en-US'}, headers=HEADER).json()['results'][0]['key'] for video in range(len(list_movie) - 1)]

    movie_data = [requests.get(f"{MOVIE_URL}{data['id']}", headers=HEADER).json() for data in datas]
    
    lists_cast = [requests.get(f"{CREDITS_URL}{data['id']}/credits", headers=HEADER).json()["cast"] for data in datas]
    characters = [Cast(cast_id=movie_data[_]["id"], name=lists_cast[_][cast]["name"], cast_img=f'{CAST_IMG}{lists_cast[_][cast]["profile_path"]}') for _ in range(len(lists_cast)) for cast in range(len(lists_cast[_]))]
    
    
    if Upcomming.query.filter(Upcomming.id).count() == 0:
        upcomming_movies = [
            Upcomming(
            id=movie_data[data - 1]["id"],
            title=movie_data[data - 1]["title"],
            overview=movie_data[data - 1]["overview"],
            banner = list_banner_data[data - 1],
            image = list_image_data[data - 1],
            movie = list_movie_data[data - 1],
            key = key[data - 1],
            date=movie_data[data - 1]["release_date"]
            )  
            for data in range(len(datas))
            ]
        db.session.add_all(upcomming_movies)
        db.session.add_all(characters)
        db.session.commit()
        return redirect(url_for("view.upcomming_data"))
    
    return redirect(url_for("view.upcomming_data"))