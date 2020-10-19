def get_user(request):
    user = request.get_argument('username')
    pw = request.get_argument('password')

    if user == 'nyc' and pw =='iheartnyc':
        return 1
    else:
        return None

login_url = '/login'