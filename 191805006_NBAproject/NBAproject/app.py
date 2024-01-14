# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 17:59:55 2024

@author: Technopc
"""
# app.py dosyası
from flask import Flask, render_template, request
from nbastats import get_nba_team_data, get_nba_player_data
from flask_fontawesome import FontAwesome

# Diğer kodlar...
app = Flask(__name__)
fa = FontAwesome(app)

@app.route('/')
def home():
    return render_template('index.html', title='Home')

@app.route('/get_nba_team_data')
def route_get_nba_team_data():
    team_data_df = get_nba_team_data()
    return render_template('team_data.html', title='NBA Team Data', data=team_data_df.to_html())

@app.route('/get_nba_player_data')
def route_get_nba_player_data():
    player_data_df = get_nba_player_data("LeBron James", "2022")
    return render_template('player_data.html', title='LeBron James Data for 2022', data=player_data_df.to_html())

if __name__ == "__main__":
    app.run(debug=True)
