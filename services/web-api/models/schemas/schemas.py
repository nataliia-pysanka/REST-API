from . import ma


class DirectorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'surname', 'date_birth', 'wiki_url')


director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


class GenreSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


class MovieSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'date_release', 'rating')


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


class PosterSchema(ma.Schema):
    class Meta:
        fields = ('id', 'url')


poster_schema = PosterSchema()
posters_schema = PosterSchema(many=True)


class RoleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'enabled')


role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nickname', 'name', 'surname', 'date_birth',
                  'date_registry')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
