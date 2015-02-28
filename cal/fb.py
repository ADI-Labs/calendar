from facebook import GraphAPI
from cal.schema import db, User, Event
from config import FACEBOOK_ACCESS_TOKEN
import iso8601

graph = GraphAPI(FACEBOOK_ACCESS_TOKEN)
page_ids = [
    '76561782869',       # SIPA
    '102471088936',      # CU
    '102771993129318',   # Medical Center
    '42316303783',       # Business School
    '1376345619301146',  # Prison Divest
    '29438666163',       # General Studies
    '432008956893415',   # Data Science Institute
    '112971615402197',   # GSAPP
    '112695952113138',   # School of Continuing Education
    '141764905854299',   # Columbia Public Health
    '126195220761399',   # College of Physicians and Surgeons
    '78606477710',       # Columbia Surgery
    '111534465576828',   # CORE
    '108772683119',      # School of Social Work
    '13795941507',       # Journalism School
    '123393449987',      # College of Dental Medicine
    # '15014549949',      # Admissions (Ignoring due to irrelevance)
    '91514290668',       # School of Nursing
    '102009214108',      # Athletics
    '109409079078868',   # Law School
    '546415562042239',   # Bacchanal
    '144606668914747',   # Institute of African Studies
    '197174936966015',   # Institute for Research in African-American Studies
    '266148036757553',   # Gospel Choir and Band
    '150090971686018',   # Middle East Institute
    '26916178394',       # Miller Theatre
    '129297810427358',   # Columbia University Archives
    '263741120328412',   # Application Development Initiative
    '230719923749613',   # Columbia Data Science Society
    '1429903290580029',  # Columbia Computer Science Preprofessional Society
    '235600359819546',   # Columbia Entrepeneurs Organization
    '741854835834184',   # Women in Computer Science
    '125692804276829',   # Columbia Wushu
    '129362477239648',   # Barnard Honor Board
    '457753504323688',   # Governing Board at Barnard
    '185837218150459',   # CU Generation
    '366678636772770',   # CU Sewa
    '235512743299366',   # CU French Cultural Society
    '183241131734731',   # Columbia Women's Business Society
    '124992620889529',   # CU Film Productions
    '179902808839135',   # CU Hindu Student Organization
    '124968174239226',   # Columbia Korean Student Association
    '496954750365809',   # Hong Kong Students and Scholars Association
    '717330888294259',   # Activities Board at Columbia
    # '40892339383',       # African Law Students Association (no access token)
    '320800730384',      # African Students Association
    '296714777168407',   # Aikido
    '520402061427273',   # American Institue of Chemical Engineers
    '1494887544128402',  # American Society of Mechanical Engineers
    '521503351319712',   # Amnesty International
    '520769028008386',   # Art of Living
    '428445673869676',   # Artist Society
    '148614427657',      # Asian American Alliance
    '375683145895890',   # Asian Pacific American Heritage Month
    '110020189713',      # Association for Computing Machinery
    '167922473231554',   # Bach Society
    '266583283465556',   # Baha'i Club
    '623118397733595',   # Ballet Ensemble
    '127184634043594',   # Beta Theta Phi
    '732370266883997',   # Bhangra
    '635929716473961',   # Biomedical Engineering Society
    '124263327769732',   # Black Organization of Soul Sisters
    '66114979956',       # Black Students' Organization
    '153912894629817',   # Black Theater Ensemble
    '567567480016627',   # Blue and White
    '359273777483537',   # Blue Key Society
    # '125787164166676',   # Canterbury Club (Unsupported request)
    '360462704017712',   # Caribbean Student Association
    '479184565457877',   # Chicano Caucus
    '238971376152821',   # China Law and Business Association (CCLBA)
    # '237160662994336',   # Chinese Bible Study Group (AUTH error)
    '36845738820',       # Chinese Students and Scholars Assoiation
    '264877036963661',   # Chinese Students Club
    '324052140074',      # Chowdah Sketch Comedy
    # '195629250527859',   # Christians on Campus (AUTH error)
    '83038617978',       # Clefhangars
    '154909354648149',   # Club Bangla
    '1506111726297876',  # College Democrats
    '629861307054701',   # College Liberatarians
    '114512668562658',   # College Republicans
    '170604546317524',   # Columbia Undergraduate Law Review
    '157090571531',      # Columbia Classical Performers
    '257020914343135',   # CCSC 2015
    '414584481937511',   # CCSC 2016
    '402055506589690',   # CCSC 2017
    # '261702970520779',   # Columbia Community Outreach (unsupported request)
    '656632027711940',   # Columbia Elections Board
    '58365309913',       # Columbia Daily Spectator
    '406947596037547',   # Columbia Economics Society
    '156469054399404',   # Columbia Engineers Without Borders
    '162282307296224',   # Columbia Financial Investment Group
    '469888179740276',   # Columbia Financial Review
    '249997198467774',   # Columbia Graduate Consulting Club
    '682327028452194',   # Columbia International Relations Council and Association
]


def update_fb_events():
    for page_id in page_ids:
        user = User.query.filter_by(id=page_id).first()
        if user is None:
            u = graph.get_object(id=page_id)
            user = User(id=page_id, name=u["name"])
            db.session.add(user)

        events = graph.get_connections(id=page_id, connection_name="events")
        events = events["data"]
        for event in events:
            event_id = int(event['id'])

            current_event = Event.query.filter_by(id=event_id).first()
            if current_event is None:
                print("New event from %s: %s" % (page_id, event['id']))
                current_event = Event(id=event_id)

            # Parse the start and end times.
            start = iso8601.parse_date(event["start_time"])
            current_event.start = start.replace(tzinfo=None)
            end = event.get('end_time', None)
            if end is not None:
                end = iso8601.parse_date(end)
                current_event.end = end.replace(tzinfo=None)

            # Update other fields.
            current_event.user = user
            current_event.location = event.get('location', None)
            current_event.name = event['name']
            current_event.url = "https://www.facebook.com/" + event['id']

            db.session.add(current_event)

    db.session.commit()
