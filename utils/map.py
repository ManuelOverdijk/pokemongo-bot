## Credits: DanielGibbs @ https://www.reddit.com/r/pokemongodev/comments/4topoi/quick_question_on_cell_ids_submitted_to_server/d5kmxxc

from s2sphere import CellId, LatLng


def get_neighbours(lat, lng):
    origin = CellId.from_lat_lng(LatLng.from_degrees(lat, lng)).parent(15)
    neighbours = {origin.id()}

    edge_neighbors = origin.get_edge_neighbors()
    surrounding_neighbors = [
        edge_neighbors[0],                          # North neighbor
        edge_neighbors[0].get_edge_neighbors()[1],  # North-east neighbor
        edge_neighbors[1],                          # East neighbor
        edge_neighbors[2].get_edge_neighbors()[1],  # South-east neighbor
        edge_neighbors[2],                          # South neighbor
        edge_neighbors[2].get_edge_neighbors()[3],  # South-west neighbor
        edge_neighbors[3],                          # West neighbor
        edge_neighbors[0].get_edge_neighbors()[3],  # North-west neighbor
    ]

    for cell in surrounding_neighbors:
        neighbours.add(cell.id())
        for cell2 in cell.get_edge_neighbors():
            neighbours.add(cell2.id())

    return neighbours
