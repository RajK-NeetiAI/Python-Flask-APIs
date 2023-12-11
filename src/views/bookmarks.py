import uuid

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.utils.bookmarks_responses import *
from src.constants.http_status_codes import *
from src.database.bookmarks_database import *


bookmarks = Blueprint(
    'bookmarks',
    __name__,
    url_prefix='/api/v1/bookmarks'
)


@bookmarks.post('/create')
@jwt_required()
def create():
    if request.is_json:
        data = request.get_json()
        url = data['url']
        remarks = data['remarks']
        bookmark = get_bookmark_by_url(url)
        if bookmark:
            return format_bookmarks_create_update_delete('Url already exists.'), HTTP_409_CONFLICT
        else:
            user = get_jwt_identity()
            bookmark = Bookmark(url=url, visits=0, shorten_url=str(
                uuid.uuid1()), remarks=remarks, user_id=user['id'])
            _ = create_bookmark(bookmark)
            return format_bookmarks_create_update_delete('Bookmark created.'), HTTP_201_CREATED
    else:
        return format_bookmarks_create_update_delete('Bad request.'), HTTP_400_BAD_REQUEST


@bookmarks.get('/get/all')
@jwt_required()
def get_all():
    user = get_jwt_identity()
    all_bookmarks = get_bookmarks(user['id'])
    return format_bookmarks_get('Success', all_bookmarks)


@bookmarks.get('/get/one/<int:id>')
@jwt_required()
def get_one(id: int):
    try:
        bookmark = get_bookmark_by_id(id)
        if bookmark:
            return format_bookmarks_get('Success.', [bookmark])
        else:
            return format_bookmarks_get('Not found.', [{}]), HTTP_204_NO_CONTENT
    except:
        return format_bookmarks_get('Not found.', [{}]), HTTP_204_NO_CONTENT


@bookmarks.post('/update/<int:id>')
@jwt_required()
def update_one(id: int):
    if request.is_json:
        try:
            user = get_jwt_identity()
            bookmark = get_bookmark_by_id(id, user['id'])
            if bookmark:
                data = request.get_json()
                update = {
                    'url': data['url'],
                    'remarks': data['remarks']
                }
                _ = update_bookmark_by_id(id, update)
                return format_bookmarks_create_update_delete('Success.'), HTTP_200_OK
            else:
                return format_bookmarks_create_update_delete('Not found.'), HTTP_204_NO_CONTENT
        except:
            return format_bookmarks_create_update_delete('Not found.'), HTTP_204_NO_CONTENT
    else:
        return format_bookmarks_create_update_delete('Bad request.'), HTTP_400_BAD_REQUEST


@bookmarks.post('/delete/<int:id>')
@jwt_required()
def delete_one(id: int):
    try:
        user = get_jwt_identity()
        bookmark = get_bookmark_by_id(id, user['id'])
        if bookmark:
            _ = update_bookmark_by_id(id, {'is_deleted': True})
            return format_bookmarks_create_update_delete('Success.'), HTTP_200_OK
        else:
            return format_bookmarks_create_update_delete('Not found.'), HTTP_204_NO_CONTENT
    except:
        return format_bookmarks_create_update_delete('Not found.'), HTTP_204_NO_CONTENT


@bookmarks.post('/get/shorten/<string:shorten_url>')
@jwt_required()
def get_shorte(shorten_url: str):
    try:
        user = get_jwt_identity()
        bookmark = get_bookmark_by_shorten_url(shorten_url, user['id'])
        if bookmark:
            _ = update_bookmark_by_id(
                bookmark['id'], {'visits': bookmark['visits'] + 1})
            return format_bookmarks_get('Success.', [bookmark])
        else:
            return format_bookmarks_get('Not found.', [{}]), HTTP_204_NO_CONTENT
    except:
        return format_bookmarks_get('Not found.', [{}]), HTTP_204_NO_CONTENT
