from lib.flask_lib import blueprints
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized
import json
from lib.serializer.generic import  generate_generic_serializer
from lib.serializer.tournament import  generate_tournament_to_dict_serializer
from lib import serializer,stripe_lib
from lib import serializer
from lib.route_decorators.db_decorators import load_tables
from sqlalchemy.orm import joinedload
from lib.flask_lib.permissions import create_tournament_permissions
from lib.serializer.deserialize import deserialize_json
from lib import orm_factories
from lib.route_decorators.auth_decorators import check_current_user_is_active

def get_tournament_field_descriptions():
    long_descriptions={}
    short_descriptions={}
    short_descriptions["queuing"]="Enable queuing"
    short_descriptions["discount"]="Offer discount"
    short_descriptions["manually_set_price"]="Ticket price"
    short_descriptions["number_of_tickets_for_discount"]="Discount on X tickets"
    short_descriptions["discount_price"]="Discount ticket price"
    short_descriptions["limited_herb"]="Limited herb"
    short_descriptions["number_of_signifigant_scores"]="# of signifigant scores"
    short_descriptions["team_tournament"]="Team tournament"
    short_descriptions["number_of_qualifiers"]="Number of qualifiers"
    short_descriptions["number_of_qualifiers_for_a_when_finals_style_is_ppo"]="Number of A qualifiers"
    short_descriptions["number_of_qualifiers_for_b_when_finals_style_is_ppo"]="Number of B qualifiers"    
    short_descriptions["tournament_name"]="Tournament name"
    short_descriptions["queue_size"]="Max size of queue"    
    short_descriptions["use_stripe"]="Use Stripe for player ticket purchases"
    short_descriptions["stripe_sku"]="Single ticket Stripe SKU "
    short_descriptions["discount_stripe_sku"]="Discount Stripe SKU "
    short_descriptions["stripe_price"]="Single ticket Stripe price"
    short_descriptions["discount_stripe_price"]="Discount Stripe price"    
    short_descriptions["minimum_number_of_tickets_allowed"]="Minimum # ticket purchase"
    short_descriptions["ticket_increment_for_each_purchase"]="Ticket increment per purchase"            
    short_descriptions["number_of_unused_tickets_allowed"]="# of unused tickets allowed"
    short_descriptions["active"]="Tournament is active"            
    short_descriptions["ifpa_rank_restriction"]="IFPA rank restriction"
    short_descriptions["team_tournament"]="Team tournament"
    short_descriptions["number_players_per_team"]="Number players per team"    
    short_descriptions["finals_style"]="Finals style"            
    short_descriptions["number_of_games_played_in_each_finals_match"]="Number of games played in each finals match"
    short_descriptions["style_of_points_assigned_during_finals"]="Finals points style"
    short_descriptions["allow_desk_purchases"]="Allow desk purchases"
    short_descriptions["allow_phone_purchases"]="Allow phone purchases"    

    
    long_descriptions["discount"]="Offer a discount if players buy a certain number of tickets"
    long_descriptions["queuing"]="Enabling queuing will allow players to be queued on machines in this tournament."
    long_descriptions["manually_set_price"]="The price of a single ticket"
    long_descriptions["number_of_tickets_for_discount"]="The number of tickets to offer a discount on.  For example, if this is set to 3 then a player will pay the discount amount when they buy 3 tickets."
    long_descriptions["discount_price"]="The discount price when the player purchases the discount amount of tickets."
    long_descriptions["limited_herb"]="If enabled, the tournament will be limited herb.  This will automatically limit the totoal number of tickets a player can purchase"
    long_descriptions["number_of_signifigant_scores"]="The number of scores that will be used for your overall ranking.  For example, if this is set to 5 then your top 5 scores on 5 seperate machines will be used to calculate your overall ranking."
    long_descriptions["team_tournament"]="Enabling this makes this tournament a team tournament.  Only players on a team will be able to buy tickets and play games in this tournament"
    long_descriptions["number_of_qualifiers"]="The number of players that will qualify"
    long_descriptions["number_of_qualifiers_for_a_when_finals_style_is_ppo"]="The number of players that will qualify for A division"
    long_descriptions["number_of_qualifiers_for_b_when_finals_style_is_ppo"]="The number of players that will qualify for B division.  Note that these players will follow the A division qualifiers.  For example, if the number of players that will qualify for A division is 16, and B division is set to 16 then the players that will qualify for B are player with rankings 16-32"    

    return {'long_descriptions':long_descriptions,'short_descriptions':short_descriptions}

@blueprints.event_blueprint.route('/tournament_description',methods=['GET'])
def get_tournament_descriptions():    
    return jsonify({'descriptions':get_tournament_field_descriptions()})

