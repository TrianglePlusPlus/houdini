from django.core.management import call_command
from django.core.management.base import BaseCommand


emails_to_delete = [
    "j3844692@nwytg.com",
    "jason@thecrop.org",
    "cuyemu@69postix.info",
    "asdfbjlasdflbjkasdf@send22u.info",
    "itcater@thecorp.org",
    "blop@georgetown.edu",
    "f@georgetown.edu",
    "ff@georgetown.edu",
    "panejefaj@20boxme.org",
    "save@0mixmail.info",
    "accessdummyone@gmail.com",
    "accessdummytwo@gmail.com",
    "accessdummythree@gmail.com",
    "yehelilo@twocowmail.net",
    "wuci@twocowmail.net",
    "g1798094@nwytg.com",
    "yeo48006@tqoai.com",
    "efm05488@ckoie.com",
    "elc22307@soioa.com",
    "nhz76623@soioa.com",
    "i1817139@nwytg.com",
    "i1820162@nwytg.com",
    "blah@thecorp.org",
    "blah2@thecor.org",
    "blah22@thecor.org",
    "blah22@thecorp.org",
    "randomuser@thecorp.org",
    "someaddress@thecorp.org",
    "foo@thecorp.org",
    "jd@corp.edu",
    "connor@corp.edu",
    "johnlahey@gmail.com",
    "bubbles@gmail.com",
    "jassange@gmail.com",
    "riley@ymail.com",
    "elliot@ymail.com",
    "justice.suh@gmail.com",
    "carlk6th@gmail.com",
    "roisinemcloughlin@gmail.com",
    "roisinmcl@hotmail.com",
    "b2701136@nwytg.net",
    "b2717377@nwytg.net",
    "vondy@mit.edu",
    "peter.johnston.xc@gmail.com",
    "pj202@georgetown.edu",
    "connorylu@gmail.com",
    "rabrabmooley@gmail.com",
]


class Command(BaseCommand):
    help = 'Delete test users no longer used to test Access'

    def handle(self, *args, **options):
        from houdini_server.models import User
        for email in emails_to_delete:
            user = User.objects.get(email=email)
            # print out their names for safe keeping
            print(user.name + ", " + user.email)
            user.delete()


# test00 - test29 - deactivate?

# dop it  dop.it@thecorp.org  ✔   it, it admin
# other matson    sam439@georgetown.edu   ✔   —
# Sally Matson    gm.it@thecorp.org   ✘   —??
# Sally Matson    sally.matson@gmail.com  ✔   it  06/07/2017 6:04 p.m.
# sally matson    sally@thecorp.org   ✔   it hr admin, c suite, it, accounting, catering, hoya snaxa, midnight mug, mug, seasonal, uncommon grounds, vital vittles, the hilltoss, it admin, marketing admin, hr, hr admin, accounting admin, timelord, catering admin, hoya snaxa admin, midnight mug admin, mug admin, seasonal admin, uncommon grounds admin, vital vittles admin, service admin, marketing, hoya snaxa hr admin
