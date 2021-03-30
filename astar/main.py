import pydot
import math
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

from classes import City

# list of cities
cities = []

# list of nodes
nodes = []

# list of images for updating the image
imgList = []


def readCity(file_name):
    # read from file and populate list of cities
    # open the file
    f = open(file_name, "r")
    # read the content of the file and store it in text
    text = f.read()
    # split the content based on new line so we get each line
    result_text = text.split("\n")
    separator_index = 0
    for line in result_text:
        # for every line in the input file
        # check if the line is empty
        if line == '':
            # line is empty, then it is the separator
            separator_index = result_text.index(line)

    # split the content of the input file into two based on the separator
    # the first half should contain the cities and their locations
    # the second half should contain the relation between cities
    chunk1 = result_text[:separator_index]
    chunk2 = result_text[separator_index+1:]

    # the first chunk is for city initialization
    for line in chunk1:
        # for every line in the first chunk
        # the name of the city is retrieved from the first character in the line
        city_name = line[0]
        # the coordinate of the city is retrieved from the third and fifth digit in the line
        city_coor = [int(line[2]), int(line[4])]
        # create a new city object and append it to the list of cities
        cities.append(City(city_name, city_coor))

    # the second chunk is for distances between cities
    for line in chunk2:
        # for every line in the second chunk
        # the source city name is retrieved from the first char in the line
        source_city_name = line[0]
        # the destination city name is retrieved from the third char in the line
        destination_city_name = line[2]
        # the distance between those cities is retrieved from the fifth until the last char in the line
        distance = int(line[4:])

        # connect cities
        # the connection is bidirectional (two-ways) so we need to add connection from both cities

        # find the source city from the list of cities
        # add the destination city and the distance to the source city object
        cities[findCity(source_city_name)].addConnectedCity(
            destination_city_name, distance)
        # find the destination city from the list of cities
        # add the source city and the distance to the destination city object
        cities[findCity(destination_city_name)].addConnectedCity(
            source_city_name, distance)


def preprocess():
    # function to generate the graph of the cities and their connections
    # read from file
    readCity("d_input.txt")

    # visualization
    # using pydot to create a graph
    graph = pydot.Dot('my_graph', graph_type='graph', bgcolor='white')
    for city in cities:
        # Add city nodes
        node = pydot.Node(city.getCityName(), shape='circle',
                          label=city.getCityName())
        # add the city node to the graph
        graph.add_node(node)
        # add the city node to the list of nodes
        nodes.append(node)
    # initialize empty list to hold the cities that has already been connected in the graph
    # because the connection is bidirectional, there will be two lines for every connection
    # to avoid that, we will skip creating the line if the city pair has already been connected
    # outer list
    already_connected = []
    for city in cities:
        # for every city in the list of cities
        # Add edges
        # get the list of destination city names of the current city
        connected_cities = city.getConnectedCities().keys()
        for c_city in connected_cities:
            # for every destination city
            # check if the destination city is already connected with the current city
            if c_city in already_connected:
                # the destination city is already connected with the current city
                # do nothing
                continue
            else:
                # the destination city hasn't been connected with the current city
                # add the current city to the list of already connected cities
                already_connected.append(city.getCityName())
                # generate the edge from the current city to the destination city
                # and the distance as the label of the edge
                graph.add_edge(pydot.Edge(city.getCityName(
                ), c_city, color='blue', label=city.getConnectedCities().get(c_city)))

    # output visualization
    # save the graph into 'output.png'
    graph.write_png('output.png')  # ignore error


def authenticate(srcCityE, destCityE, textVar):
    # function to check whether the input is empty or not
    # get the input of source city entry
    source_city = srcCityE.get()
    # get the input of destination city entry
    destination_city = destCityE.get()
    # check if any of those entries are empty or not
    if source_city == '' or destination_city == '':
        # entry is empty
        messagebox.showwarning("Warning", "Your entry may be empty!")
    else:
        # entry is filled
        # initialize a list of city names from the list of cities
        cities_list = [city.getCityName() for city in cities]
        # check if the entry is in the list of city names or not
        if not source_city in cities_list or not destination_city in cities_list:
            # entry is not in the list of city names
            messagebox.showwarning("Warning", "Your entry is not defined!")
        else:
            # entry is in the list of city names
            # initialize a local variable to store the source city object
            source_city = cities[findCity(source_city)]
            # initialize a local variable to store the destination city object
            destination_city = cities[findCity(destination_city)]
            # update the image based on the destination city
            # see the updateImage function for explanation of the argument
            updateImage(destination_city)
            # initialize path variable as the name of the source city
            path = [source_city.getCityName()]
            # execute the A Star Search function with these arguments
            # fyi, textVar is the string variable to display the path to the GUI
            aStarSearch(source_city, destination_city, path, textVar)


def aStarSearch(src, dest, path, textVar):
    # a star algorithm / function
    # check if the current source city is the destination city
    if isDestination(src, dest):
        # the current source city is the destination city
        # set the string variable textVar to the path variable
        # (meaning update the label to the visited cities from the
        # source city until the destination city)
        textVar.set(path)
        # this is the recursive break point
    else:
        # the current source city is not the destination city
        # find shortest f from each edge
        distance_list = []  # list of distances (f distances)
        city_names = []  # list of city names
        for city in src.getConnectedCities().keys():
            # for every connected cities from the source city
            # calculate the euclidean distance for the connected city to the destination city
            # or it is usually called as the heuristic distance / straight line distance
            ed = euclideanDistance(cities[findCity(city)], dest)
            # distance
            # total the heuristic distance of the connected city to the destination city
            # with the distance from the source city to the connected city
            # or it is usually referred to as f
            d = src.getConnectedCities().get(city) + ed  # f
            # append the total distance or f distance to the list of distances
            distance_list.append(d)
            # append the connected city to the list of city names
            city_names.append(city)

        # check if the source city has no connection to get to other cities
        if not distance_list or not city_names:
            # the source city doesnt have connections
            textVar.set("No path found!")
        else:
            # the source city has connections
            # calculate the shortest f distance
            shortest_index = distance_list.index(min(distance_list))
            # set the next_city variable to the least f distance of the source city
            next_city = cities[findCity(city_names[shortest_index])]

            # if city has been visited before
            new_distance_list = []  # new list of f distances
            new_city_names = []  # new list of city names
            for city in city_names:
                # for every city in list of city names
                # display the boolean of whether the city is already visited or not
                print(f"{city} in path: {city in path}")
                # check if the city is in path or has been visited before
                if city in path:
                    # city has been visited before
                    # check if there are no connected cities from this city
                    if not distance_list or not city_names:
                        # there are no connected cities from this city
                        # stop loop
                        textVar.set("No path found!")
                        break
                    else:
                        # there are connections from this city
                        # do nothing
                        pass
                else:
                    # city hasn't been visited before
                    # append the city's f distance to the new list of f distances
                    new_distance_list.append(
                        distance_list[city_names.index(city)])
                    # append the city's name to the new list of city names
                    new_city_names.append(city)
                    # calculate the shortest f distance from the new list of f distances
                    shortest_index = new_distance_list.index(
                        min(new_distance_list))
                    # set the next_city variable to the shortest f distance
                    next_city = cities[findCity(
                        new_city_names[shortest_index])]

            # check if there are no connected cities for the current connected city
            if not new_distance_list or not new_city_names:
                # the current connected city has no connections
                textVar.set("No path found!")
            else:
                # the current connected city has connections
                # display the source city name
                print(f"src city: {src.getCityName()}")
                # intialize tmp as a dictionary with the new list of city names as the key
                # and the new list of f distances as the value
                tmp = dict(zip(new_city_names, new_distance_list))
                # display the current connected cities of the source city and their f distances
                print(f"connected cities: {tmp.keys()}{tmp.values()}")
                # display the next city (selected city) from the source city
                print(f"next city: {next_city.getCityName()}")
                print("\n")

                # append the next city's name to the path (meaning visited)
                path.append(next_city.getCityName())
                # call this function again (recursive) with the next city as the new source city
                # this will run until the destination city is found or until there are no connections left
                aStarSearch(next_city, dest, path, textVar)


def findCity(city_name):
    # function to find city from list of cities using city name
    # initialize outer list
    city_names = []
    for c in cities:
        # for every city is the list of citites
        # append the city name to the outer list
        city_names.append(c.getCityName())
    # return the index of the city_name to caller
    return city_names.index(city_name)


def isDestination(src, dest):
    # function to check whether the source city is the destination city or not
    # check if the source city coordinates is equal to the destination city coordinates or not
    if src.getCoor() == dest.getCoor():
        # the source city coordinates is equal to the destination city coordinates
        return True
    else:
        # the source city coordinates is not equal to the destination city coordinates
        return False


def euclideanDistance(a, b):
    # function to calculate straight line distance between city a and city b
    p1 = a.getCoor()
    p2 = b.getCoor()
    # distance = sqrt((p2.x - p1.x)^2 + (p2.y - p1.y)^2)
    dist = math.sqrt(math.pow((p2[0]-p1[0]), 2) + math.pow((p2[1]-p1[1]), 2))
    # return the distance to caller
    return dist


def updateImage(dest):
    # function to update the current image
    # initialize a pydot graph
    graph = pydot.Dot('my_graph', graph_type='graph', bgcolor='white')
    for city in cities:
        # for every city in the list of cities
        # Add nodes
        # calculate the heuristic distance of this city to destination city
        ed = euclideanDistance(city, dest)
        ed = round(ed)
        # create a node with the heuristic distance as the xlabel
        node = pydot.Node(city.getCityName(), shape='circle',
                          label=city.getCityName(), xlabel=f"{city.getCityName()}(h={ed})")
        # add the node to the graph
        graph.add_node(node)

    # initialize an empty list for the already connected cities
    already_connected = []
    for city in cities:
        # for every city in the list of cities
        # Add edges
        connected_cities = city.getConnectedCities().keys()
        for c_city in connected_cities:
            # for every destination city
            # check if the destination city is already connected to the current city
            if c_city in already_connected:
                # the destination city is already connected
                # do nothing
                continue
            else:
                # the destination city is not connected
                # append the current city to the already connected list
                already_connected.append(city.getCityName())
                # add an edge fro the current city to the destination city with the distance as the label
                graph.add_edge(pydot.Edge(city.getCityName(
                ), c_city, color='blue', label=city.getConnectedCities().get(c_city)))

    # output visualization
    # save the graph to 'output.png' as an image
    graph.write_png('output.png')  # ignore error
    # open the image and set the current image to the newly created image
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

    # bind the button to execute authenticate function
    button1.configure(command=lambda: authenticate(entry1, entry2, text_var))


# main
preprocess()  # execute the preprocess functoin
window = Tk()  # initialize Tkinter GUI
initGUI(window)  # initialize Tkinter GUI widgets
window.mainloop()  # run the GUI
