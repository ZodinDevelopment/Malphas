import os
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, send_from_directory, jsonify, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app import db
from app.media.forms import UploadVideoForm, CommentForm, UploadPhotoForm, EmptyForm
from app.models import User, Video, Post, Comment, Photo
from app.media import bp


def allowed_image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['IMAGE_EXTENSIONS']


def allowed_video_file(filename):
    return '.' in filename and filename.rsplit(".", 1)[1].lower() in current_app.config['VIDEO_EXTENSIONS']


@bp.route("/dev_channel", methods=['GET', 'POST'])
def dev_channel():
    #form = EmptyForm()
    page = request.args.get('page', 1, type=int)
    videos = Video.query.order_by(Video.timestamp.desc()).paginate(
        page, current_app.config['MEDIA_PER_PAGE'], False
    )
    next_url = url_for('media.dev_channel', page=videos.next_num) if videos.has_next else None
    prev_url = url_for('media.dev_channel', page=videos.prev_num) if videos.has_prev else None

    return render_template('media/dev_channel.html', title="Dev Channel", videos=videos.items, next_url=next_url, prev_url=prev_url)


@bp.route('/video/<video_id>', methods=['GET', 'POST'])
def video(video_id):
    video = Video.query.filter_by(id=video_id).first_or_404()
    all_vids = Video.query.order_by(Video.timestamp.desc())
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_anonymous:
            flash("Only users can comment.")
            return redirect(url_for('media.video', video_id=video_id))
            
        comment = Comment(body=form.comment.data, video=video, author=current_user)
        db.session.add(comment)
        db.session.commit()
        flash("Comment submitted.")
        return redirect(url_for("media.video", video_id=video_id))
    
    page = request.args.get('page', 1, type=int)
    comments = Comment.query.filter_by(video=video).order_by(Comment.timestamp.desc()).paginate(
        page, current_app.config['ITEMS_PER_PAGE'], False
    )
    next_url = url_for('media.video', video_id=video_id, page=comments.next_num) if comments.has_next else None
    prev_url = url_for('media.video', video_id=video_id, page=comments.prev_num) if comments.has_prev else None

    return render_template('media/video.html', title=video.title, video=video, comments=comments.items, form=form, next_url=next_url, prev_url=prev_url, all_vids=all_vids)


@bp.route('/watch/<video_id>')
def watch(video_id):
    video = Video.query.filter_by(id=video_id).first_or_404()

    return send_from_directory(os.path.join(current_app.config['UPLOAD_FOLDER'], 'videos'), video.filename)



@bp.route("/upload_video", methods=['GET', 'POST'])
@login_required
def upload_video():
    if current_user.email not in current_app.config['ADMINS']:
        flash("You are not authorized to access this page.")
        return redirect(url_for('main.index'))

    form = UploadVideoForm()
    if form.validate_on_submit():
        f = form.upload.data
        
        if not allowed_video_file(f.filename):
            flash("Invalid file type")
            return redirect(url_for('media.upload_video'))

        filename = secure_filename(f.filename)
        f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'videos', filename))
        video = Video(title=form.title.data, description=form.description.data, filename=filename)

        db.session.add(video)
        db.session.commit()
        flash("Video uploaded successfully.")
        return redirect(url_for('media.video', video_id=video.id))

    return render_template('media/upload_video.html', title="Upload Video", form=form)


@bp.route("/upload_photo", methods=['GET', 'POST'])
@login_required
def upload_photo():
    if current_user.email not in current_app.config['ADMINS']:
        flash("You are not authorized to access this page.")
        return redirect(url_for('main.index'))

    form = UploadPhotoForm()
    if form.validate_on_submit():
        f = form.upload.data

        if not allowed_image_file(f.filename):
            flash("Invalid file type")
            return redirect(url_for("media.upload_photo"))

        filename = secure_filename(f.filename)
        f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'photos', filename))
        photo = Photo(title=form.title.data, filename=filename)

        db.session.add(photo)
        db.session.commit()

        flash("Photo uploaded")
        return redirect(url_for('media.gallery'))

    return render_template('media/upload_photo.html', title="Upload Photo", form=form)


@bp.route('/gallery')
def gallery():
    page = request.args.get('page', 1, type=int)
    photos = Photo.query.order_by(Photo.timestamp.desc()).paginate(
        page, current_app.config['MEDIA_PER_PAGE'], False
    )
    next_url = url_for('media.gallery', page=photos.next_num) if photos.has_next else None
    prev_url = url_for('media.gallery', page=photos.prev_num) if photos.has_prev else None

    return render_template('media/gallery.html', title="Gallery", photos=photos.items, next_url=next_url, prev_url=prev_url)

    
    
@bp.route('/image/<photo_id>')
def image(photo_id):
    photo = Photo.query.filter_by(id=photo_id).first_or_404()
    return send_from_directory(os.path.join(current_app.config['UPLOAD_FOLDER'], 'photos'), photo.filename)

    
