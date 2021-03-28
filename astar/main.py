import pydot
import math
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

from classes import City

# list of cities
cities = []

# list of nodes for the graph
nodes = []

# for updating the image
imgList = []


def readCity(file_name):
    # read from file and populate list of cities
    f = open(file_name, "r")
    text = f.read()
    # split file text into two based on new line
    result_text = text.split("\n")
    separator_index = 0
    for line in result_text:
        if line == '':
            separator_index = result_text.index(line)

    chunk1 = result_text[:separator_index]
    chunk2 = result_text[separator_index+1:]

    # the first chunk is for city initialization
    for line in chunk1:
        city_name = line[0]
        city_coor = [int(line[2]), int(line[4])]
        cities.append(City(city_name, city_coor))

    # the second chunk is for distances between cities
    for line in chunk2:
        source_city_name = line[0]
        destination_city_name = line[2]
        distance = int(line[4:])
        # connect cities
        cities[findCity(source_city_name)].addConnectedCity(
            destination_city_name, distance)
        cities[findCity(destination_city_name)].addConnectedCity(
            source_city_name, distance)


def preprocess():
    # function to graph input cities into objects
    # read from file
    readCity("d_input.txt")

    # visualization
    graph = pydot.Dot('my_graph', graph_type='graph', bgcolor='white')
    for city in cities:
        # Add nodes
        node = pydot.Node(city.getCityName(), shape='circle',
                          label=city.getCityName())
        graph.add_node(node)
        nodes.append(node)

    already_connected = []
    for city in cities:
        # Add edges
        connected_cities = city.getConnectedCities().keys()
        for c_city in connected_cities:
            if c_city in already_connected:
                continue
            else:
                already_connected.append(city.getCityName())
                graph.add_edge(pydot.Edge(city.getCityName(
                ), c_city, color='blue', label=city.getConnectedCities().get(c_city)))

    # output visualization
    graph.write_png('output.png')  # ignore error


def authenticate(srcCityE, destCityE, textVar):
    # function to check whether the input is empty or not
    source_city = srcCityE.get()
    destination_city = destCityE.get()
    if source_city == '' or destination_city == '':
        # input is empty
        messagebox.showwarning("Warning", "Your entry may be empty!")
    else:
        # input is filled
        cities_list = [city.getCityName() for city in cities]
        if not source_city in cities_list or not destination_city in cities_list:
            # input is not in cities
            messagebox.showwarning("Warning", "Your entry is not defined!")
        else:
            source_city = cities[findCity(source_city)]
            destination_city = cities[findCity(destination_city)]
            updateImage(destination_city)
            path = [source_city.getCityName()]
            aStarSearch(source_city, destination_city, path, textVar)


def aStarSearch(src, dest, path, textVar):
    # a star algorithm
    if isDestination(src, dest):
        textVar.set(path)
    else:
        # find shortest f from each edge
        distance_list = []  # list distance or value
        city_names = []  # list keys
        for city in src.getConnectedCities().keys():
            # euclidean distance
            ed = euclideanDistance(cities[findCity(city)], dest)
            # distance
            d = src.getConnectedCities().get(city) + ed  # f
            distance_list.append(d)
            city_names.append(city)

        # check if there are no connected cities
        if not distance_list or not city_names:
            textVar.set("No path found!")
        else:
            shortest_index = distance_list.index(min(distance_list))
            next_city = cities[findCity(city_names[shortest_index])]

            # if city has been visited before
            new_distance_list = []
            new_city_names = []
            for city in city_names:
                print(f"{city} in path: {city in path}")
                if city in path:
                    # check if there are no connected cities
                    if not distance_list or not city_names:
                        textVar.set("No path found!")
                        break
                    else:
                        #print(f"remove {city} from {city_names}")
                        # distance_list.pop(city_names.index(city))
                        # city_names.remove(city)
                        #shortest_index = new_distance_list.index(min(new_distance_list))
                        #next_city = cities[findCity(new_city_names[shortest_index])]
                        pass
                else:
                    new_distance_list.append(
                        distance_list[city_names.index(city)])
                    new_city_names.append(city)
                    shortest_index = new_distance_list.index(
                        min(new_distance_list))
                    next_city = cities[findCity(
                        new_city_names[shortest_index])]

            # check if there are no connected cities
            if not new_distance_list or not new_city_names:
                textVar.set("No path found!")
            else:
                print(f"src city: {src.getCityName()}")
                tmp = dict(zip(new_city_names, new_distance_list))
                print(f"connected cities: {tmp.keys()}{tmp.values()}")
                print(f"next city: {next_city.getCityName()}")
                print("\n")

                path.append(next_city.getCityName())
                aStarSearch(next_city, dest, path, textVar)


def findCity(city_name):
    # function to find city from list of cities using city name
    city_names = []
    for c in cities:
        city_names.append(c.getCityName())
    return city_names.index(city_name)


def isDestination(src, dest):
    # function to check whether the source city is the destination city or not
    if src.getCoor() == dest.getCoor():
        return True
    else:
        return False


def euclideanDistance(a, b):
    # function to calc straight line distance between city a and city b
    p1 = a.getCoor()
    p2 = b.getCoor()
    dist = math.sqrt(math.pow((p2[0]-p1[0]), 2) + math.pow((p2[1]-p1[1]), 2))
    return dist


def updateImage(dest):
    # visualization
    graph = pydot.Dot('my_graph', graph_type='graph', bgcolor='white')
    for city in cities:
        # Add nodes
        ed = euclideanDistance(city, dest)
        ed = round(ed)
        node = pydot.Node(city.getCityName(), shape='circle',
                          label=city.getCityName(), xlabel=f"{city.getCityName()}(h={ed})")
        graph.add_node(node)

    already_connected = []
    for city in cities:
        # Add edges
        connected_cities = city.getConnectedCities().keys()
        for c_city in connected_cities:
            if c_city in already_connected:
                continue
            else:
                already_connected.append(city.getCityName())
                graph.add_edge(pydot.Edge(city.getCityName(
                ), c_city, color='blue', label=city.getConnectedCities().get(c_city)))

    # output visualization
    graph.write_png('output.png')  # ignore error
    img = Image.open("output.png")
    img = ImageTk.PhotoImage(img)
    imgList[0].configure(image=img)
    imgList[0].image = img


def initGUI(root):
    # function to initialize tkinter GUI
    root.title("AIN-PA1")
    # root.geometry('800x400')

    # frames
    frameLeft = Frame(root)
    frameLeft.pack(side=LEFT, padx=10, pady=10)
    frameRight = Frame(root)
    frameRight.pack(side=RIGHT, expand="true", fill="both", padx=10, pady=10)

    # image view
    img = Image.open("output.png")
    #img = img.resize((400, 400), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(frameLeft, image=img)
    panel.image = img
    imgList.append(panel)  # global var
    panel.grid(column=0, row=0)

    # entry
    label1 = Label(frameRight, text="Source City:")
    label1.grid(column=1, row=0, sticky=E)
    entry1 = Entry(frameRight, width=10)
    entry1.grid(column=2, row=0)
    label2 = Label(frameRight, text="Destination City:")
    label2.grid(column=1, row=1, sticky=E)
    entry2 = Entry(frameRight, width=10)
    entry2.grid(column=2, row=1)
    button1 = Button(frameRight, text="Execute")
    button1.grid(column=1, row=3, columnspan=2, sticky='NESW')

    # result
    label3 = Label(frameRight, text="Result:")
    label3.grid(column=1, row=4, sticky=E)
    text_var = StringVar()
    text_var.set("...")
    label4 = Label(frameRight, textvariable=text_var)
    label4.grid(column=2, row=4, sticky=W)

    button1.configure(command=lambda: authenticate(entry1, entry2, text_var))


# main
preprocess()
window = Tk()
initGUI(window)
window.mainloop()
