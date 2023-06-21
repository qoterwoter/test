from django.core.mail import send_mail


def send_notification_email(user_email, order):
    subject = 'На ваш заказ оставлен новый отклик!'
    message = f'Новый отклик водителя оставлен на ваш заказ: {order}'
    from_email = 'your_email@example.com'
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)


def send_driver_notifications(order):
    from .models import Driver
    drivers = Driver.objects.all()

    for driver in drivers:
        if driver.notifications:
            subject = 'Доступен новый заказ'
            message = f'В приложении доступен новый заказ!\n\n' \
                      f'Детали заявки:\n' \
                      f'Откуда: {order.from_location}\n' \
                      f'Куда: {order.to_location}\n' \
                      f'Время отправления: {order.departure_time}\n' \
                      f'Количество взрослых: {order.men_amount}\n' \
                      f'Количество детей: {order.children_amount}\n' \
                      f'Комментарий: {order.comment}\n' \
                      f'Зайдите на сайт, чтобы первым откликнуться на нее.'
            from_email = 'your_email@example.com'
            recipient_list = [driver.user.email]
            send_mail(subject, message, from_email, recipient_list)
