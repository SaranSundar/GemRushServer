import heapq
from dataclasses import dataclass
from typing import List, Dict

from marshmallow_dataclass import dataclass as mmdc

from card.card_data import Card
from card.deck import Deck
from card.noble import Noble
from enums.Tier import Tier
from enums.TokenColor import TokenColor
from game.game_state import GameState
from player.player import PlayerState
from room.room import Room
from utils.utils import get_response, RequestMethods, parse_response, ApiMethods


@dataclass
@mmdc
class SimulationPlayer:
    id: str


@dataclass
@mmdc
class Simulation:
    deck: Deck
    room: Room
    game_state: GameState
    players: List[SimulationPlayer]
    host_ip: str = "http://207.246.122.46"
    port: str = "9378"

    def create_host(self) -> SimulationPlayer:
        host = SimulationPlayer(id="Saran")
        self.players = [host]
        return host

    def create_other_players(self):
        other_players = ["Vishruth", "Juwhan", "Rooshi", "Joseph Mama"]
        for player_id in other_players:
            self.players.append(SimulationPlayer(id=player_id))

    def create_room(self, host: SimulationPlayer) -> Room:
        create_room_response = get_response(
            RequestMethods.POST,
            f"{self.host_ip}:{self.port}{ApiMethods.CREATE_ROOM}",
            {
                "name": "Simulation Testing Room",
                "password": "computers-fight",
                "min_players": 2,
                "max_players": 4,
                "creator_id": host.id,
                "score_to_win": 15
            })

        return parse_response(Room, create_room_response)

    def join_room(self, player: SimulationPlayer, room: Room) -> Room:
        join_room_response = get_response(
            RequestMethods.POST,
            f"{self.host_ip}:{self.port}{ApiMethods.JOIN_ROOM}/{room.id}",
            {
                "name": room.name,
                "password": room.password,
                "player_id": player.id
            })
        return parse_response(Room, join_room_response)

    def start_game(self, room: Room) -> GameState:
        start_game_response = get_response(
            RequestMethods.POST,
            f"{self.host_ip}:{self.port}{ApiMethods.START_GAME}",
            {
                'room_id': room.id
            })

        return parse_response(GameState, start_game_response)

    @staticmethod
    def calc_weight_of_all_cards(game_state: GameState, player: SimulationPlayer):
        # points of card
        # cost of card, number of tokens needed
        # does card color get closer to noble
        # tokens bank has
        player_state: PlayerState = game_state.player_states[player.id]
        # colors needed for nobles
        # colors needed for more expensive cards on board
        # Cost to buy card, points card offers when bought, does card get you closer to noble
        pq = []
        deck = game_state.deck
        board: Dict[Tier, List[Card]] = deck.board
        for tier in board:
            tier_cards = board[tier]
            for card in tier_cards:
                heapq.heappush(pq, Simulation.calc_weight_of_card(player_state, card, deck.bank, deck.noble_cards))
        return pq

    @staticmethod
    def calc_weight_of_card(player_state: PlayerState, card: Card, bank: Dict[TokenColor, int],
                            nobles: List[Noble]):
        card_points = card.points
        # Calculate token cost for card and what tokens bank has
        needed_tokens_that_are_in_bank: int = 0
        card_token_cost = 0
        for token_color in card.cost:
            discount = player_state.calculate_permanent_token_discount(token_color)
            if discount >= card.cost[token_color]:
                # Requires no tokens of this color
                pass
            else:
                # Requires number of tokens minus number of cards of that color
                needed_tokens = card.cost[token_color] - discount
                card_token_cost += needed_tokens
                if token_color in bank:
                    # Add if bank has an available token of the color that is needed
                    needed_tokens_that_are_in_bank += 1

        # Check if card gets you closer to a noble
        closer_to_noble = False
        for noble in nobles:
            if card.color in noble.cost:
                closer_to_noble = True
                break

        return card_points - card_token_cost - needed_tokens_that_are_in_bank + closer_to_noble

    def take_turn(self, room: Room, player: SimulationPlayer, game_state: GameState):
        pq = Simulation.calc_weight_of_all_cards(game_state, player)

    def start_simulation(self):
        # The host creates the room
        host = self.create_host()
        self.room = self.create_room(host)
        # Other players join the room
        for player in self.players:
            if player.id != host.id:
                self.room = self.join_room(player, self.room)

        # Host starts game
        self.game_state = self.start_game(self.room)
