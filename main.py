import sqlite3
from functools import reduce
from itertools import chain
from itertools import cycle

airline_bd = sqlite3.connect('Airline.db')
airports_bd = sqlite3.connect("Airports.db")
parking_bd = sqlite3.connect("Parking.db")
airline_cur = airline_bd.cursor()
airports_cur = airports_bd.cursor()
parking_cur = parking_bd.cursor()



#1. Посчитать рентабельность рейсов
def flights_profitability():
    flights = list(zip(*airline_cur.execute(f'SELECT jet_id, arrival_point, ticket_price, number_of_tickets_sold, depreciation_cost, fuel_cost FROM Flights').fetchall()))
    jet_id, airports = flights[0], flights[1]
    models = [airline_bd.execute(f'SELECT model_name FROM "Jets" WHERE jet_id == "{i}"').fetchone()[0] for i in jet_id]
    classes = [airline_bd.execute(f'SELECT class_name FROM "Models" WHERE model_name == "{i}"').fetchone()[0] for i in models]
    maintenance_cost = [airports_bd.execute(f'SELECT maintenance_cost FROM "{airports[i]}" WHERE class == "{classes[i]}"').fetchone()[0] for i in range(len(airports))]
    income = sum(list(map(lambda x, y: x * y, flights[2], flights[3])))
    expenses = sum(flights[4]) + sum(flights[5]) + sum(maintenance_cost)
    return (income - expenses) / expenses


#2. Посчитать налет самолетов (за месяц, например)
def flight_time():
    jet_id = list(chain(*airline_cur.execute(f'SELECT jet_id FROM Jets').fetchall()))
    travel_times_list = [airline_bd.execute(f'SELECT travel_time FROM Flights WHERE jet_id == "{i}"').fetchall() for i in jet_id]
    return dict(zip(jet_id, [sum(list(chain(*lists_of_lists))) for lists_of_lists in travel_times_list]))


#3. Посчитать “заполняемость” рейса в % за месяц.
def flight_occupancy():
    flights = list(zip(*airline_cur.execute(f'SELECT flight_id, jet_id, number_of_tickets_sold FROM Flights').fetchall()))
    flight_id, jet_id, number_of_tickets_sold = flights[0], flights[1], flights[2]
    models = [airline_bd.execute(f'SELECT model_name FROM "Jets" WHERE jet_id == "{i}"').fetchone()[0] for i in jet_id]
    number_of_passangers = [airline_bd.execute(f'SELECT number_of_passengers FROM "Models" WHERE model_name == "{i}"').fetchone()[0] for i in models]
    ratio = list(map(lambda x, y: round(x / y, 2), number_of_tickets_sold, number_of_passangers))
    return dict(zip(flight_id, ratio))

#4. Посчитать стоимость простоя самолетов.
def parking_cost():
    jet_id = list(chain(*airline_cur.execute(f'SELECT jet_id FROM Jets').fetchall()))
    models = [airline_bd.execute(f'SELECT model_name FROM "Jets" WHERE jet_id == "{i}"').fetchone()[0] for i in jet_id]
    classes = [airline_bd.execute(f'SELECT class_name FROM "Models" WHERE model_name == "{i}"').fetchone()[0] for i in models]
    airports = list(chain(*parking_cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()))
    airports.remove('sqlite_sequence')
    parking_hours = [[parking_cur.execute(f'SELECT "hours" FROM "{i}" WHERE jet_id == "{j}"').fetchall()[0][0] for i in airports] for j in jet_id]
    airports_hours_dict = list(dict(zip(airports, i)) for i in parking_hours)
    cost_dict = [[airports_bd.execute(f'SELECT parking_cost FROM "{key}" WHERE class == "{classes[i]}"').fetchone()[0]*val for key, val in airports_hours_dict[i].items()] for i in range(len(classes))]
    return sum(map(sum, cost_dict))

print(flights_profitability())
print(flight_time())
print(flight_occupancy())
print(parking_cost())
