# Django


Django is a Python framework designed for creating web applications from front to back. It is free and open source.
It takes care of most of the annoying and complicated parts of a website such as database design and management, handling HTTP requests, and rendering HTML pages with information from the back-end.

The Django Project provides a great tutorial: https://docs.djangoproject.com/en/2.1/intro/

A Django application consists of four main parts:
  1. Models
    - These are like objects and directly correspond to database tables
    - Django manages the database through automatically generated 'migrations'. This allows the developer to use it with any database technology (MySQL, PostgreSQL, SQLite) by simply changing the settings and running migrations
    - Django provides built-in methods for dealing with models such as:
      ```python
      Corgi.objects.create(**kwargs) # Create a Corgi using keyword args for its attributes
      Corgi.objects.all() # Get all Corgi objects from the database
      Listing.objects.raw('SELECT * FROM corgi_store_corgi WHERE age_years > 3') # Get all corgis older than 3
      ```
     - By extending Django's built-in Model object, these three lines can be used to enable creation, deletion, and searching Favorites ([link](https://github.com/Lshoemake/CSC346Project2/blob/master/corgi_store/models.py#L59-L61)):
      ```python
      class Favorite(models.Model):
          user = models.ForeignKey(User, on_delete=models.CASCADE)
          corgi = models.ForeignKey(Corgi, on_delete=models.CASCADE)
      ```
     - Django also provides built-in user sign-up, authentication, and sessions as well as an Admin dashboard for managing users and database entries

  2. URLs
    - By simply providing a list of 'paths', a developer can easily manage all of the valid paths on the website and connect the paths of views which will render a template
    - The following URLs provide paths for the homepage, a page for viewing all corgis, and a page for buying corgis ([link](https://github.com/Lshoemake/CSC346Project2/blob/master/corgi_store/urls.py#L5-L17)):
      ```python
      urlpatterns = [
          path('', views.home, name='home'),
          path('corgi/all/', views.browse_corgis, name='browse_corgis'),
          path('corgi/buy/', views.buy_corgi, name='buy_corgi'),
      ]
      ```

  3. Views
    - Views are just methods that are run when a user visits the URL that points to that view
    - A view can perform some operations and must return a HttpResponse object by either rendering an HTML template or redirecting to a different URL
    - For example, the `corgi/buy/` URL above calls this view which renders the `buy.html` template with all corgis that are for sale ([link](https://github.com/Lshoemake/CSC346Project2/blob/master/corgi_store/views.py#L28-L29)):
      ```python
      def buy_corgi(request):
          return render(request, 'buy.html', {'listings': Listing.objects.filter(open=True)})
      ```

  4. Templates
    - Templates are used by the `render` function in views. They are HTML pages that contain some Jinja2 syntax for templating with variables from Django
    - The following excerpt of `buy.html` shows templating variables into an HTML page showing corgi information ([link](https://github.com/Lshoemake/CSC346Project2/blob/master/corgi_store/templates/buy.html#L132-L134)):
      ```html
      <b>Name: </b>{{ listing.corgi.name }}<br>
      <b>Gender: </b>{{ listing.corgi.gender }} <br>
      <b>Age: </b>{{ listing.corgi.age_years }} years, {{ listing.corgi.age_months }} months <br>
      ```
     - Templates can also implement control structures such as loops and if-else statements


Basically, when a user visits a URL, Django compares that URL to the paths in `urls.py` which can include regex. Once a match is found, Django uses the view specified by the URL to perform an action such as creating or favoriting a corgi. The view then returns an HttpResponse object by using `render()` with a template and some variables to populate the template with (called 'context') or by redirecting to a different URL using `redirect()` and the new URL's name (not path).


Simple example:
  - User clicks 'Buy a Corgi' in menu bar which contains `href="{% url 'buy_corgi' %}"`
  - Django finds the 'buy_corgi' URL from `urls.py` and calls `buy_corgi()` view:
    ```python
    def buy_corgi(request):
        return render(request, 'buy.html', {'listings': Listing.objects.filter(open=True)})
    ```
  - This view simply returns the HttpResponse object created by rendering the `buy.html` template with all open listings


For a slightly more complicated example, consider favoriting a corgi (demonstrate this in browser):
  - When a logged-in user clicks the empty heart by a corgi on the browse page, the following Javascript is run ([link](https://github.com/Lshoemake/CSC346Project2/blob/master/corgi_store/templates/browse.html#L141-L153)):
    ```javascript
    function favorite(id)
    {
    	var heart = document.getElementById("favorite"+id);
    	heart.innerHTML = '<span class="glyphicon glyphicon-heart" style="color:red;" onclick="unfavorite('+id+')"></span>'
      console.log("ajax");
      $.post({
            url: '/favorite/',
            data: {
              corgi: id
            },
            dataType: 'json',
          });
    }
    ```
   - This will send a POST request to `/favorite/` with JSON data containing the corgi's ID
   - The `/favorite` URL will call the `favorite_corgi` view ([link](https://github.com/Lshoemake/CSC346Project2/blob/master/corgi_store/views.py#L81-L89)):
    ```python
    def favorite_corgi(request):
        if request.method == 'POST':
            corgi = Corgi.objects.get(id=request.POST.get('corgi'))
            fav = Favorite.objects.filter(user=request.user, corgi=corgi)
            if not fav:
                Favorite.objects.create(user=request.user, corgi=corgi)
            else:
                fav[0].delete()
        return redirect('browse_corgis')
    ```
  - If this view receives a POST request, it will load the corgi object specified by the ID, then determine if the corgi is already favorited. If not, then it will create the Favorite object in the table. Otherwise, it will delete the existing favorite object.
  - It always returns `redirect('browse_corgis')` to re-render the browse page since we do not want the user to be redirected to the `/favorite/` URL which is just an API end point
