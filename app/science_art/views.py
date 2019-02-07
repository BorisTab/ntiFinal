from flask import Blueprint


blueprint = Blueprint('sciart', 'sciart')


@blueprint.route('/', methods=['GET'])
def main():
    # JS код в этом темплейте не работает (бесконечный цикл)
    # НЕ ЗАПУСКАТЬ НА СЛАБОМ ЖЕЛЕЗЕ -- УРОНИТ!!!
    # return render_template('science-art.html')
    return '200'
