from django.shortcuts import render
from .models import Person, Perk
import cv2
import shutil
from os import path

# Add functions here.
def add_person_to_db(first_name : str, last_name : str, pin : int):
    person = Person(first_name=first_name, last_name=last_name, pin=pin)
    person.save()

def add_perk_to_db(name : str):
    perk = Perk(name=name)
    perk.save()


def get_perks_from_db():
    return Perk.objects.all()
    
def get_people_from_db():
    return Person.objects.all()

def get_person_from_db(this_pin):
    return Person.objects.filter(pin = this_pin)

        
def get_html_ready_perks(query):
    context = {"perks":[]}
    inc = 0
    for i in query:
        context["perks"].append({
            "id": i.id,
            "name": i.name,
            "date_added": i.date_added.date,
            "time_added": i.date_added.time,
        })
        inc += 1
    return context

def get_html_ready_people(query):
    context = {"people":[]}
    inc = 0
    for i in query:
        context["people"].append({
            "id": i.id,
            "first_name": i.first_name,
            "last_name": i.last_name,
            "pin": i.pin,
            "date_added": i.date_added.date,
            "time_added": i.date_added.time,
        })
        inc += 1
    return context


def take_picture(url):
    cam = cv2.VideoCapture(0)
    cv2.namedWindow('Webcam screenshot - Press Space!')

    while True:
        ret, frame = cam.read()
        

        cv2.imshow('Press Space to take Picture', frame)
        
        k  = cv2.waitKey(1)

        # if space pressed
        if k%256  == 32:
            imgSaveDir = path.join( "./person_images/",url)

            cv2.imwrite(imgSaveDir, frame)

            break
    
    cam.release()
    # shutil.move(url,"./person_images/",copy_function)
    # cam.destoryAllWindows()



# Create your request views here.
def enroll_new_person(request):
    info = request.POST
    
    # person = Person()

    perks = []
    lname = ''
    fname = ''
    pin = ''
    for i in info:
        if i.isnumeric(): # perks
            perks.append(Perk.objects.get(id=int(i)))
        elif i == "first_name":
            fname = info[i]
        elif i == "last_name":
            lname = info[i]
        elif i == "pin":
            pin = info[i]
    
    person = Person.objects.create(first_name=fname, last_name=lname, pin=pin)
    
    for i in perks:
        person.perks.add(i)

    url = str(person.id) + '.png'
    # print(person.objects.all())

    # get id of that person from database
    person.image = url
    person.save()

    take_picture(url)
    

    # debugging
    # print(f'\n\n\n\n\n\n\n\n\n{url} moved to {images_folder}')
    return show_manage_people(request)


def show_home(request):
    # # Person.objects.all().delete()
    # person = Person(first_name="Joe", last_name="Trump", image="maga.png")
    # person.pin = "5000"
    # person.save()
    # person = Person(first_name="Donald", last_name="Biden", pin="5050", image=".png")
    # person.save()
    # print(Person.objects.all())
    # Perk.objects.all().delete()
    print(Perk.objects.all())
    return render(request, "home.html")

def show_scan(request):
    
    perks_query = get_perks_from_db()
    context = get_html_ready_perks(perks_query)

    return render(request, "scan.html", context)

def show_pic(request):
    pin = request.POST["pin"]
    url = ''
    
    if pin:
        person = get_person_from_db(pin)
    
        url = str(person.id) + '.png'
    
    perks_query = get_perks_from_db()
    context = get_html_ready_perks(perks_query)
    context['image'] = url
    print('\n\n\n',context)
    return render(request,'scan.html', context)

def show_manage_perks(request):
    perks_query = get_perks_from_db()
    context = get_html_ready_perks(perks_query)
    print(context)
    return render(request, "manage_perks.html", context)

def add_perk(request):
    perk_name = request.POST["perk"]
    add_perk_to_db(perk_name)
    return show_manage_perks(request)

def show_manage_people(request):
    people_query = get_people_from_db()
    context = get_html_ready_people(people_query)

    print(context)
    return render(request, "manage_people.html", context)

def show_add_person(request):
    perks_query = get_perks_from_db()
    context = get_html_ready_perks(perks_query)
    return render(request, "add_person.html", context)

def show_edit_person(request, id):
    # print(f"ID: {id}")
    person = Person.objects.get(id=id)
    context = { "person": {
            "id": person.id,
            "first_name": person.first_name,
            "last_name": person.last_name,
            "pin": person.pin,
            "person_perks": [],
        }
    }

    for i in person.perks.all():
        context["person"]["person_perks"].append(str(i.id))
    
    context["perks"] = {}

    all_perks = Perk.objects.all()
    
    inc = 0
    for i in all_perks:
        context["perks"][str(i.id)] = {"name": i.name}
        inc += 1
    
    print(context)
    
    return render(request, "edit_person.html", context)

def make_edit(request, id):
    person = Person.objects.get(id=id)
    url = person.image
    person.delete()

    info = request.POST
    
    # person = Person()

    perks = []
    lname = ''
    fname = ''
    pin = ''
    for i in info:
        if i.isnumeric(): # perks
            perks.append(Perk.objects.get(id=int(i)))
        elif i == "first_name":
            fname = info[i]
        elif i == "last_name":
            lname = info[i]
        elif i == "pin":
            pin = info[i]
    
    new_person = Person.objects.create(first_name=fname, last_name=lname, pin=pin)
    
    for i in perks:
        new_person.perks.add(i)

    # print(person.objects.all())

    # get id of that person from database
    new_person.image = url
    new_person.save()
    return show_manage_people(request)

def make_delete(request, id):
    person = Person.objects.get(id=id)
    person.delete()
    return show_manage_people(request)

def update_person(request):
    new_info = request.POST
    pass

def delete_person(request):
    info = request.POST
    pass

def delete_perk(request):
    pass