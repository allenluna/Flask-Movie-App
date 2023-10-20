from flask import Blueprint, request, render_template, jsonify
from flask_login import current_user
from flask_cors import cross_origin
from .model import Movies, Cast, Popular, Upcomming, Mylist
from . import db
import requests
from .post_movie import MOVIE_VIDEO, YOUTUBE_EMBED, CREDITS_URL, HEADER
import random
from datetime import datetime


view = Blueprint("view", __name__)


# mylist to JSON type
def mylist_data(data):
    return {
        "id" : data.id,
        "title" : data.title,
        "overview" : data.overview,
        "banner" : data.banner,
        "image" : data.image,
        "movie" : data.movie,
        "key" : data.key,
        "reviews" : data.reviews,
        "author_review" : data.author_review,
        "date" : data.date
    }


@view.route("/", methods=["GET", "POST"])
def home():
    movies = Movies.query.all()
    popular = Popular.query.all()
    upcomming = Upcomming.query.all()
    
    videos = f"{MOVIE_VIDEO}{459003}/videos"

    # Trailers
    trailer_response = requests.get(videos, params={"language": "en-US"}, headers=HEADER)
    trailer_data = trailer_response.json()["results"]
    get_all_trailer = [f'{YOUTUBE_EMBED}{trailer_data[trailer]["key"]}' for trailer in range(len(trailer_data))]
    upcomming_trailer = get_all_trailer[0]


    if request.method == "POST":
        search = request.get_json()
        
        movieTitle = Movies.query.filter(Movies.title.like(f"%{search['search']}%")).all()
        upcommingTitle = Upcomming.query.filter(Upcomming.title.like(f"%{search['search']}%")).all()
        popularTitle = Popular.query.filter(Popular.title.like(f"%{search['search']}%")).all()
        list_data = [movieTitle, upcommingTitle, popularTitle]
        new_list = [list_data[list][new_list] for list in range(len(list_data)) for new_list in range(len(list_data[list]))]
            
        return jsonify({"data": [{
            'id' : movie.id,
            'title':movie.title,
            'image': movie.image
            } 
        for movie in new_list]})

    return render_template("index.html", movies=movies, populars=popular, upcomming=upcomming, upcomming_trailer=upcomming_trailer ,current_user=current_user)

@view.route("/movie-data")
def movie_data():
    movie = Movies.query.all()
    banner_movie = [[trailer.movie, trailer.key] for trailer in movie]
    banner = random.choice(banner_movie)
    return render_template("movies.html", movies=movie, banner=banner)

@view.route("/popular-data")
def popular_data():
    popular = Popular.query.all()
    banner_popular = [[trailer.movie, trailer.key] for trailer in popular]
    banner = random.choice(banner_popular)
    return render_template("popular.html", populars=popular, banner=banner)

@view.route("/upcomming-data")
def upcomming_data():
    upcomming = Upcomming.query.all()
    banner_popular = [[trailer.movie, trailer.key] for trailer in upcomming]
    banner = random.choice(banner_popular)

    return render_template("upcomming.html", upcomming=upcomming, banner=banner)

@view.route("/preview")
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def preview():
    pop_id = request.args.get("pop_id")
    movie_id = request.args.get("movie_id")
    upcom_id = request.args.get("upcom_id")
    
    if pop_id:
        popular = Popular.query.get(pop_id)
        cast = Cast.query.filter_by(cast_id=pop_id).all()
        videos = f"{MOVIE_VIDEO}{pop_id}/videos"
        # Trailers
        trailer_response = requests.get(videos, params={"language": "en-US"}, headers=HEADER)
        trailer_data = trailer_response.json()["results"]
        get_all_trailer = [f'{YOUTUBE_EMBED}{trailer_data[trailer]["key"]}' for trailer in range(len(trailer_data))]
        return render_template("preview.html", all_trailer=get_all_trailer, popular=popular, casts=cast, current_user=current_user)
    elif movie_id:
        movies = Movies.query.get(movie_id)
        cast = Cast.query.filter_by(cast_id=movie_id).all()
        videos = f"{MOVIE_VIDEO}{movie_id}/videos"
        # Trailers
        trailer_response = requests.get(videos, params={"language": "en-US"}, headers=HEADER)
        trailer_data = trailer_response.json()["results"]
        get_all_trailer = [f'{YOUTUBE_EMBED}{trailer_data[trailer]["key"]}' for trailer in range(len(trailer_data))]

        return render_template("preview.html", all_trailer=get_all_trailer, movies=movies, casts=cast,current_user=current_user)

    else:
        upcomming = Upcomming.query.get(upcom_id)
        cast = Cast.query.filter_by(cast_id=upcom_id).all()
        videos = f"{MOVIE_VIDEO}{upcom_id}/videos"
        # Trailers
        trailer_response = requests.get(videos, params={"language": "en-US"}, headers=HEADER)
        trailer_data = trailer_response.json()["results"]
        get_all_trailer = [f'{YOUTUBE_EMBED}{trailer_data[trailer]["key"]}' for trailer in range(len(trailer_data))]

        return render_template("preview.html", all_trailer=get_all_trailer, upcomming=upcomming, casts=cast, current_user=current_user)

# add mylist data
@view.route("/my-added-lists")
def added_lists():
    return render_template("mylist.html", current_user=current_user)


@view.route("/mylist-item")
def mylist():
    popular_id = request.args.get("popular_id")
    movie_id = request.args.get("movie_id")
    upcomming_id = request.args.get("upcomming_id")
    if popular_id:
        popular = Popular.query.get(popular_id)

        check_id_exists = Mylist.query.filter_by(id=popular.id).first()

        if not check_id_exists:
            mylist = Mylist(
                id = popular.id,
                title=popular.title,
                overview=popular.overview,
                banner=popular.banner,
                image=popular.image,
                movie=popular.movie,
                key=popular.key,
                reviews=popular.reviews,
                author_review=popular.author_review,
                date=datetime.now().strftime("%Y-%m-%d"),
                user_name=current_user
            )
            db.session.add(mylist)
            db.session.commit()
            return {"results" : mylist_data(mylist)}
        else:
            return {"results" : "Already added in a lists."}
    elif upcomming_id:
        upcomming = Upcomming.query.get(upcomming_id)

        check_id_exists = Mylist.query.filter_by(id=upcomming.id).first()

        if not check_id_exists:
            mylist = Mylist(
                id = upcomming.id,
                title=upcomming.title,
                overview=upcomming.overview,
                banner=upcomming.banner,
                image=upcomming.image,
                movie=upcomming.movie,
                key=upcomming.key,
                reviews=upcomming.reviews,
                author_review=upcomming.author_review,
                date=datetime.now().strftime("%Y-%m-%d"),
                user_name=current_user
            )
            db.session.add(mylist)
            db.session.commit()
            return {"results" : mylist_data(mylist)}
        else:
            return {"results" : "Already added in a lists."}
    elif movie_id:
        movie = Movies.query.get(movie_id)

        check_id_exists = Mylist.query.filter_by(id=movie.id).first()

        if not check_id_exists:
            mylist = Mylist(
                id = movie.id,
                title=movie.title,
                overview=movie.overview,
                banner=movie.banner,
                image=movie.image,
                movie=movie.movie,
                key=movie.key,
                reviews=movie.reviews,
                author_review=movie.author_review,
                date=datetime.now().strftime("%Y-%m-%d"),
                user_name=current_user
            )
            db.session.add(mylist)
            db.session.commit()
            return {"results" : mylist_data(mylist)}
        else:
            return {"results" : "Already added in a lists."}
        
@view.route("/mylist-delete")
def list_delete():
    delete_id = request.args.get("delete")
    list_to_delete = Mylist.query.get(delete_id)
    db.session.delete(list_to_delete)
    db.session.commit()
    return {"results" : "Deleted"}