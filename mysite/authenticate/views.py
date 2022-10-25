from random import randint
from django.shortcuts import render
from .models import Person, Perk
import cv2
import shutil
import time
from pynput.keyboard import Key, Controller
keyboard = Controller()
from os import path, remove

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
    try:
        person = Person.objects.get(pin = this_pin)
        print("~~~~~\nperson found by pin!\n~~~~~")
    except:
        person = False    
        print("~~~~~\nperson NOT found by pin!\n~~~~~")
    return person

def add_zero_padding(num : str, length):
    if len(num) == length:
        return num
    if len(num) < length:
        num = "0" + num
        return add_zero_padding(num, length)

def get_rand_pin():
    while True:
        pin = add_zero_padding(str(randint(0, 999999)), 6)
        if get_person_from_db(pin) == False: # if pin not in use
            break
    return pin
        
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
    #cv2.namedWindow('Webcam screenshot - Press Space!')
    
    ret, frame = cam.read()

    cv2.imshow('Press Space to take Picture', frame)

    # time.sleep(2)
    #swap tabs
    # keyboard.press(Key.alt)
    # keyboard.press(Key.shift)
    # keyboard.press(Key.tab)
    # keyboard.release(Key.tab)
    # keyboard.release(Key.shift)
    # keyboard.release(Key.alt)

    time.sleep(.8)
    keyboard.press(Key.alt)
    keyboard.press(Key.shift)
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    keyboard.release(Key.shift)
    keyboard.release(Key.alt)

    # time.sleep(2)
    # keyboard.press(Key.alt)
    # keyboard.press(Key.shift)
    # keyboard.press(Key.tab)
    # keyboard.release(Key.tab)
    # keyboard.release(Key.shift)
    # keyboard.release(Key.alt)
        
    while True:
        ret, frame = cam.read()

        cv2.imshow('Press Space to take Picture', frame)
        
        
        k  = cv2.waitKey(1)


        # if space pressed
        if k%256  == 32:
            imgSaveDir = path.join( "./authenticate/static/", url)

            cv2.imwrite(imgSaveDir, frame)
            print(path.abspath(url))


            break
    
    cam.release()
    # shutil.move(url,imgSaveDir)
    cv2.destroyAllWindows()



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

    context = {"error": f"{fname} enrolled with pin: {pin}"}
    
    person = get_person_from_db(pin)
    
    if person == False:
        person = Person.objects.create(first_name=fname, last_name=lname, pin=pin)
        
        for i in perks:
            person.perks.add(i)

        url = str(person.id) + '.png'
        # print(person.objects.all())

        # get id of that person from database
        person.image = url
        person.save()
        take_picture(url)


    else: 
        context["error"] = "Unable to add person! PIN already in use."

    

    # debugging
    # print(f'\n\n\n\n\n\n\n\n\n{url} moved to {images_folder}')
    return show_manage_people(request, context)


def show_home(request):
    
    """
    Use the following commands to clear the database of all objects
    """
    # Person.objects.all().delete()
    # Perk.objects.all().delete()
    
    return render(request, "home.html")


def show_manage_perks(request):
    perks_query = get_perks_from_db()
    context = get_html_ready_perks(perks_query)
    #print(context)
    return render(request, "manage_perks.html", context)

def add_perk(request):
    perk_name = request.POST["perk"]
    add_perk_to_db(perk_name)
    return show_manage_perks(request)

def show_manage_people(request, error_context={"error": ""}):
    people_query = get_people_from_db()
    context = get_html_ready_people(people_query)
    context["error"] = error_context["error"]

    # print(context)
    return render(request, "manage_people.html", context)

def show_add_person(request):
    perks_query = get_perks_from_db()
    context = get_html_ready_perks(perks_query)
    context["pin"] = get_rand_pin()
    return render(request, "add_person.html", context)

def show_edit_person(request, id):
    """
        - id
        - fname
        - lname
        - pin
        - all perks own by person
            - id
            - name
        - all other perks
            - id
            - name
        JSON......
        {
            "first_name"  : fname,
            "last_name"   : lname,
            "pin"         : pin,
            "person_perks": [id<str>, id<str>, id<str>],
            "all_perks": {{id<str>:name}...}
        }
    """
    # We get the person to edit.
    person = Person.objects.get(id=id)

    # We begin populating context with person info and an empty dict for perks. 
    context = {
        "id": person.id,
        "first_name": person.first_name,
        "last_name": person.last_name,
        "pin": person.pin,
        "person_perks": [],
        "perks": []
        # "perks": [{'id': 1, 'name': 'Magic'},{...},{...}],
        # "perks": {"1": "magic", "2": "X"}
    }

    # Here, we add the perk id's (as strings) into the person_perks list.
    for i in person.perks.all():
        context["person_perks"].append(str(i.id))

    # We get all the perks from the db table.
    all_perks = Perk.objects.all()
    
    # Here, we add a data for the perks dict.
    for i in all_perks:
        # I get the id from the current perk.
        perk_id = str(i.id)
        # I get the name from the current perk.
        perk_name = i.name
        context["perks"].append(
            {
                "id"  : perk_id,
                'name': perk_name
            }
        )

        # # I add the name to the perk_id in the perks dict. 
        # context["perks"][perk_id] = perk_name
    
    # print(context)
    
    return render(request, "edit_person.html", context)

def make_edit(request, id):
    person = Person.objects.get(id=id)
    url = person.image
    person.delete()

    info = request.POST
    
    # person = Person()
    # print(f'\n\n{info}\n\n')

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

# DEL PERSON
def make_delete(request, id):
    person = Person.objects.get(id=id)

    # delete person picture
    image = person.image
    imgSaveDir = path.join( "./authenticate/static/", image)

    if path.exists(imgSaveDir):
        remove(imgSaveDir)

    person.delete()
    return show_manage_people(request)

# DEL PERK
def delete_perk(request, id):
    perk = Perk.objects.get(id=id)
    perk.delete()
    return show_manage_perks(request)


def show_scan(request, context=None):
    if context == None:
        is_verified = '0'
        selected = []
        image = "default.jpg"
        name = ''
    else:
        is_verified = context["is_verified"]
        selected = context["selected"]
        image = context['image']
        name = context['name']

        
    
    perks_query = get_perks_from_db()
    context = get_html_ready_perks(perks_query)



    context['is_verified'] = is_verified
    selected = map(lambda x: int(x),selected)

    # print([*selected])
    # print(context['perks'])

    context["selected"] = [*selected]
    context["image"] = image
    context['name'] = name


    return render(request, "scan.html", context)

def verify(request):
    info = request.POST
    selected = []
    
    for i in info:
        if i.isnumeric(): # perks
            selected.append(str(i))
        elif i == 'pin':
            pin = info[i]
    

    person = get_person_from_db(pin)

    if person == False:
        pass
        context = {
            'is_verified': "0",
            "selected": selected,
            'image': "default.jpg",
            'name': "PIN not used."
        }
    else:
        is_verified = '0'

        for i in person.perks.all():
            perk_id = str(i.id)
            if perk_id in selected:
                is_verified = '1'
                break
        
        # selected = map(lambda x: int(x),selected)
        # print([*selected])

        if int(is_verified) == 1:
            message = f"Welcome, {person.first_name}!"
        else:
            message = f'{person.first_name} SHALL NOT PASS!!'

        context = {
            'is_verified': is_verified,
            "selected": selected,
            'image': person.image,
            'name': message
            # 'perks': []
        }

    
    return show_scan(request, context)


# def show_pic(request):
#     pin = request.POST["pin"]
#     url = ''
    
#     if pin:
        
    
#         url = str(person.id) + '.png'
    
#     perks_query = get_perks_from_db()
#     context = get_html_ready_perks(perks_query)
#     context['image'] = url
#     print('\n\n\n',context)
#     return render(request,'scan.html', context)