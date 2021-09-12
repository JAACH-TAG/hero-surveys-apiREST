# src/models/routes.py
def init_api(api):
    from .auth import MeApi, RegisterApi, LoginApi, RefreshApi
    from .survey import ManipulateSurveyApi, GetUrlApi, GetSurveyApi, RedirectToUrlApi, UpdateSurveyApi, DeleteSurveyApi, StatsApi
    from .feedback import FeedbackApi
    # auth
    api.add_resource(MeApi, '/user/me')
    api.add_resource(LoginApi, '/user/login')
    api.add_resource(RegisterApi, '/user/register')
    api.add_resource(RefreshApi, '/user/refresh')
    # survey
    api.add_resource(ManipulateSurveyApi, '/survey')
    api.add_resource(GetUrlApi, '/s/<string:url>')
    api.add_resource(RedirectToUrlApi, '/<string:short_url>')
    api.add_resource(GetSurveyApi, '/survey/<int:id>')
    api.add_resource(UpdateSurveyApi, '/survey/<int:id>')
    api.add_resource(DeleteSurveyApi, '/survey/<int:id>')
    api.add_resource(StatsApi, '/survey/stats')
    # feedback
    api.add_resource(FeedbackApi, '/feedback/submit')
