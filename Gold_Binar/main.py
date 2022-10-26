from flask import Flask, jsonify, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
import pandas as pd
import sqlite3

app = Flask(__name__)

###############################################################################################################
app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info = {
        'title': LazyString(lambda:'API Documentation for Data Processing and Modeling'),
        'version': LazyString(lambda:'1.0.0'),
        'description': LazyString(lambda:'Dokumentasi API untuk Data Processing dan Modeling')
        }, host = LazyString(lambda: request.host)
    )
swagger_config = {
        "headers":[],
        "specs":[
            {
            "endpoint":'docs',
            "route":'/docs.json'
            }
        ],
        "static_url_path":"/flasgger_static",
        "swagger_ui":True,
        "specs_route":"/docs/"
    }
swagger = Swagger(app, template=swagger_template, config=swagger_config)

###############################################################################################################
# Buat connection ke db SQLite
connection = sqlite3.connect('/Users/Akbar/Desktop/Gold_Binar/Gold_Binar.db')

cursor = connection.cursor()

###############################################################################################################
# Panggil table tweet sebagai 'df'
# code di bawah komen ini
df = pd.read_sql_query("SELECT Tweet from data",connection)

###############################################################################################################
# Buat function simple cleasing misal 'frame' yang logic nya adalah sbb 
# 1. insert df
# 2. copy df menjadi df_get
# 3. buat kolom baru new_tweet yang isinya adalah kolom tweet yang di lower
# 4. kemudian rubah df_get menjadi dict dengan orient='index' dengan nama variable misal 'json' *bisa search cara nya
# 5. return atau output nya adalah variable 'json'
# contoh :
# def frame(df):
#     ...
#     return json
# code di bawah komen ini
# ...

df =pd.DataFrame(df, columns=['Tweet'])

def frame(df):
    df_get = df.copy()
    df_get['new_tweet'] = df_get['Tweet'].str.lower()
    json = df_get.to_dict(orient='index')
    return json

###############################################################################################################
# welcome message
@swag_from("docs/index.yml", methods=['GET'])
@app.route('/', methods=['GET'])
def test():
	return jsonify({'message' : 'Welcome to Tweet CRUD Api!'})

###############################################################################################################
# GET All Tweet
# 1. Buat Route dan swagger '/tweet' dengan method 'GET'
# 2. Buat function 'returnAll' yang mana bertujuan untuk memanggil function 'frame' di atas untuk cleasing data 'df'
# 3. Output atau return dari returnAll adalah json
# 4. Code di bawah komen ini

@swag_from("docs/index.yml", methods=['GET'])
@app.route('/tweet', methods=['GET'])

def returnAll():
    json = frame(df)
    return jsonify(json)


###############################################################################################################
# GET Spesifik Tweet
# Buat Route dan swagger UI yang dinamis '/tweet/<id>' dengan method 'GET'
# buat function 'returnOne' yang mana bertujuan untuk memanggil function 'frame' di atas untuk cleasing data 'df' dengan spesifik id
# logic fuction
# 1. Insert df
# 2. buat varible 'df_get' yang merupakan 'df' yang di filter berdasarkan spesifik id
# 3. gunakan function 'frame' diatas untuk cleansing 'df_get'
# 4. output atau return dari returnAll adalah json
# code di bawah komen ini

# @swag_from("docs/lang_get.yml", methods=['GET'])
# @app.route('/lang/<id>', methods=['GET'])
# def returnOne(id):  
#     ......
#     return jsonify(json)

@swag_from("docs/tweet_get.yml", methods=['GET'])
@app.route('/tweet/<id>', methods=['GET'])
def returnOne(id):
    json = frame(df)
    id = int(id)
    json = json[id]
    return jsonify(json)


###############################################################################################################
# POST Json
# 1. Buat Route dan swagger UI '/tweet' dengan method 'POST'
# 2. buat function 'returnOne' yang membaca json dengan format
# {"Tweet" : "........."}
# 3. kemudian misal di varible kan sebagai "new_tweet"
# clue --> new_tweet = {"Tweet": request.json['Tweet']}
# 4. json "new_tweet" tesebut di rubah menjadi pandas dngan nama "pd_new_tweet"
# 5. pandas "pd_new_tweet" di samakan format nya dengan table "Tweet" yang ada di SQLite agar bisa di append
# 6. append pandas tesebut
# 7. keluar kan output json "new_tweet" tadi
# code di bawah komen ini
# ...

@swag_from("docs/tweet_post.yml", methods=['POST'])
@app.route("/tweet", methods=["POST"])
def addOne():
    new_tweet = {"Tweet": request.json['Tweet']}
    pd_new_tweet = pd.DataFrame(new_tweet, columns =['new_tweet'])
    sqlite_insert_query = """INSERT INTO Tweet
                          (Tweet) 
                           VALUES 
                          (pd_new_tweet)"""
    return jsonify(new_tweet)


###############################################################################################################
# POST Upload
# 1. Buat Route dan swagger UI '/tweet/upload' dengan method 'POST'
# 2. Buat function 'addUpload' yang membaca file upload
# 3. Buat fuction addUpload
# clue --> file = request.files['file']
# 4. Kemudian file upload tesebut di baca sebagai pandas dengan read_csv misal sebagai df_upload
# 5. Samakan format df_upload dengan table "Tweet" yang ada di SQLite agar bisa di append
# 6. keluar kan output json "df_upload" tadi

@swag_from("docs/tweet_post.yml", methods=['POST'])
@app.route("/tweet/upload", methods=["POST"])

def addUpload():
    file = request.files['file']
    df_upload = pd.read_csv(file)
    df_upload = pd.DataFrame(df_upload, columns = ['Tweet'])
    sqlite_insert_query = """INSERT INTO Tweet
                          (Tweet) 
                           VALUES 
                          (df_upload)"""
    return jsonify(df_upload)

###############################################################################################################
# Run Flask
if __name__ == "__main__":
    app.run()
