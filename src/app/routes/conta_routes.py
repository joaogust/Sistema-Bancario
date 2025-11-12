from flask import render_template, Blueprint, request, redirect, url_for, jsonify, session

from src.app.services.auth_services import *

bp = Blueprint('conta', __name__)
