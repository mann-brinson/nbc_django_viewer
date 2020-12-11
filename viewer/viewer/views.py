import mysql.connector

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import SearchForm
from . import queries

class Connection():
    def __init__(self):
        self.mydb = self.create_db()
        self.cursor = self.create_cursor()

    def create_db(self): #called by __init__
        mydb = mysql.connector.connect(host="localhost",user="inf551",password='inf551',database='drug',auth_plugin='mysql_native_password')
        return mydb

    def create_cursor(self): #called by __init__
        cursor = self.mydb.cursor(buffered=True)
        return cursor

def search(request):
    '''Accept the query strings from the user.'''

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            #Extract query strings from form
            form_data = request.POST.copy()
            start_date = form_data['start_date']
            end_date = form_data['end_date']

            # context gets passed to the html template
            context = {'form': form}

            conn = Connection() #Crecte db connection
            #Construct query to get treatments
            print('start_date: ', start_date)
            print('end_date: ', end_date)
            cmd = queries.search_torr(start_date, end_date) #NOTE: Must look like YYYY-MM-DD

            conn.cursor.execute(cmd)
            results = conn.cursor.fetchall()
            print('result: ', results)

            #Add each result to the context
            result_list = []
            features = ['torr_id', 'name', 'rarbg_added', 'size', 'size_units',
            'n_seed', 'n_leech', 'torr_url', 'infohash', 'imdb_id',
            'title', 'n_keywords']
            for row in results:
                ent = dict()
                for idx, feat in enumerate(features):
                    if feat == 'rarbg_added': 
                        ent[feat] = row[idx].strftime('%Y-%m-%d')
                    else:
                        ent[feat] = row[idx]
            #     prod = row[0]
            #     ent['link'] = f'{prod}'
                result_list.append(ent)
            context['results'] = result_list
            #return HttpResponse("Good job.")
            return render(request, 'viewer/search.html', context)
    else:
        form = SearchForm()
        context = {'form': form}

    return render(request, 'viewer/search.html', context)