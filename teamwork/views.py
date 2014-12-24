from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.dispatch import receiver
from django.core.urlresolvers import reverse

from sendgrid_events.signals import sendgrid_email_received
from .models import Team, Work


@receiver(sendgrid_email_received, sender=None)
def receive(sender, **kwargs):
    print 'received'
    data = kwargs.get('data')
    team_tuple = Team.objects.get_or_create(email=data['sender_email'])
    print team_tuple
    person = team_tuple[0]
    if team_tuple[1]:
        person.name=data['sender_name']
        person.save()
    work_tuple = Work.objects.get_or_create(person=person,
                                            date=datetime.now())
    print work_tuple
    work_done = work_tuple[0]
    work_done.work = work_done.work + '\n' + data['body']
    work_done.save()


def send():
    # Sending out mails at the end of each day.
    # Needs implimentation
    pass
