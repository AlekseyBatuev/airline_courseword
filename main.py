import sqlite3

airline_db = sqlite3.connect('Airline.db')
airports_db = sqlite3.connect("Airports.db")
airline_cur = airline_db.cursor()
airports_cur = airports_db.cursor()

airline_cur.execute("""CREATE TABLE IF NOT EXISTS Airports (
	airport_ID	INTEGER NOT NULL UNIQUE,
	maintenance_cost	REAL NOT NULL,
	parking _ost	REAL NOT NULL,
	PRIMARY KEY("airport_ID" AUTOINCREMENT)
)""")

airline_cur.execute("""CREATE TABLE IF NOT EXISTS Class (
	class_ID	INTEGER NOT NULL UNIQUE,
	class_name	TEXT NOT NULL,
	flight_range	REAL NOT NULL,
	runway_length	REAL NOT NULL,
	maintenance_cost	REAL NOT NULL,
	PRIMARY KEY("class_ID" AUTOINCREMENT)
)""")

airline_cur.execute("""CREATE TABLE IF NOT EXISTS Flights (
	flight_ID	INTEGER NOT NULL UNIQUE,
	date	TEXT NOT NULL,
	airport_ID	TEXT NOT NULL,
	jet_ID	INTEGER NOT NULL,
	ticket_price	REAL NOT NULL,
	number_of_tickets_sold	INTEGER NOT NULL,
	depreciation_cost	REAL NOT NULL,
	arrival_point	TEXT NOT NULL,
	fuel_cost	REAL NOT NULL,
	PRIMARY KEY("flight_ID" AUTOINCREMENT)
)""")

airline_cur.execute("""CREATE TABLE IF NOT EXISTS Model (
	model_ID	INTEGER NOT NULL UNIQUE,
	model_name	TEXT NOT NULL,
	crew	TEXT NOT NULL,
	number_of_passengers	INTEGER NOT NULL,
	operating_cost	REAL NOT NULL,
	PRIMARY KEY("model_ID" AUTOINCREMENT)
)""")

airline_db.commit()


# 1. Посчитать рентабельность рейсов
def flights_profitability():
    flights = list(map(list, zip(*airline_cur.execute(
        f'SELECT jet_class, arrival_point, ticket_price, number_of_tickets_sold, depreciation_cost, fuel_cost FROM Flights').fetchall())))
    jet_classes, airports = flights[0], flights[1]
    print(airports)
    maintenance_cost = [airports_db.execute(
        f'SELECT maintenance_cost FROM "{airports[i]}" WHERE class == "{jet_classes[i]}"').fetchone()[0] for i in
                        range(len(airports))]
    print(maintenance_cost)
    income = sum(list(map(lambda x, y: x * y, flights[2], flights[3])))
    expenses = sum(flights[4]) + sum(flights[5]) + sum(maintenance_cost)
    return (income - expenses) / expenses


# 2. Посчитать налет самолетов (за месяц, например)
def flight_time():
    jet_classes = list(map(lambda x: x[0], airline_cur.execute(f'SELECT class FROM Jet_classes').fetchall()))
    print(jet_classes)
    for val in airline_cur.execute(f'SELECT travel_time FROM Flights WHERE jet_class == "{jet_classes[2]}"'):
        print(val)
    travel_times_list = [airline_db.execute(f'SELECT travel_time FROM Flights WHERE jet_class == "{jet_class}"').fetchall() for jet_class in jet_classes]
    #print(travel_times_list)
    travel_times = []
    for i in travel_times_list:
        summ = 0
        for j in i:
            for k in j:
                summ += k
        travel_times.append(summ)
    #print(travel_times)
    return dict(zip(jet_classes, travel_times))


print(flights_profitability())
print(flight_time())
print("ДОБАВИЛ СВОЙ КОД")
print("hui")
print("")
