from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
import json
import re
from datetime import datetime
import logging
import random

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatBot:
    def __init__(self):
        self.responses = {
            # Greetings
            'greeting': [
                "Hello! I'm your EcoByte assistant. How can I help you today?",
                "Hi there! Welcome to EcoByte. What would you like to know?",
                "Greetings! I'm here to help with EcoByte. What can I do for you?",
                "Welcome! How can I assist you with EcoByte today?",
                "Hello! Ready to help reduce food waste? What would you like to know?",
                "Hey! I'm your EcoByte buddy. How can I help?",
                "Good day! I'm here to assist with EcoByte. What's on your mind?",
                "Hi! Ready to make a difference? How can I help?",
                "Hello! Let's work together to reduce waste. What can I do for you?",
                "Welcome to EcoByte! I'm here to guide you. What would you like to know?"
            ],
            
            # Help
            'help': [
                "I can help you with:\n1. Food donation\n2. Food collection\n3. Safety guidelines\n4. Account management\n5. Registration\nWhat would you like to know?",
                "Here's what I can help with:\n1. Donating food\n2. Collecting food\n3. Safety rules\n4. Account settings\n5. Sign up process\nWhat interests you?",
                "I can guide you through:\n1. Donation process\n2. Collection steps\n3. Safety protocols\n4. Account help\n5. Registration\nWhat would you like to learn?",
                "Let me help you with:\n1. Food sharing\n2. Food receiving\n3. Safety tips\n4. Profile management\n5. Getting started\nWhat do you need?",
                "I'm here to assist with:\n1. Food donations\n2. Food collections\n3. Safety measures\n4. Account setup\n5. Registration process\nHow can I help?",
                "I can support you with:\n1. Donation guidance\n2. Collection help\n3. Safety information\n4. Account assistance\n5. Sign-up process\nWhat would you like to know?",
                "I can provide information about:\n1. Food donation\n2. Food collection\n3. Safety guidelines\n4. Account features\n5. Registration steps\nWhat interests you?",
                "I can help you understand:\n1. Donation process\n2. Collection system\n3. Safety requirements\n4. Account management\n5. Registration details\nWhat would you like to learn?",
                "I can explain:\n1. How to donate\n2. How to collect\n3. Safety protocols\n4. Account features\n5. Registration process\nWhat do you need help with?",
                "I can guide you on:\n1. Food donation\n2. Food collection\n3. Safety measures\n4. Account setup\n5. Registration steps\nWhat would you like to know?"
            ],
            
            # Donor
            'donor': [
                "As a donor, you can:\n1. List surplus food\n2. Set pickup times\n3. Connect with collectors\n4. Track donations\n5. Get recognition\nTo start, register as a donor!",
                "Donors are essential! You can:\n1. Share extra food\n2. Choose pickup times\n3. Meet collectors\n4. Monitor impact\n5. Earn recognition\nJoin as a donor today!",
                "Being a donor means:\n1. Listing food items\n2. Scheduling pickups\n3. Helping others\n4. Tracking impact\n5. Getting recognized\nReady to make a difference?",
                "As a donor, you'll:\n1. Post food listings\n2. Arrange pickups\n3. Meet collectors\n4. Track donations\n5. Get rewards\nStart donating today!",
                "Donors can:\n1. Share surplus food\n2. Set pickup schedules\n3. Connect with collectors\n4. Monitor donations\n5. Earn points\nJoin as a donor now!",
                "Being a donor allows you to:\n1. List excess food\n2. Schedule pickups\n3. Help others\n4. Track impact\n5. Get recognition\nReady to start?",
                "Donors have access to:\n1. Food listing tools\n2. Pickup scheduling\n3. Collector network\n4. Impact tracking\n5. Reward system\nBecome a donor today!",
                "As a donor, you get to:\n1. Share food items\n2. Set pickup times\n3. Meet collectors\n4. Track donations\n5. Earn rewards\nJoin us now!",
                "Donors can enjoy:\n1. Easy food listing\n2. Flexible pickups\n3. Collector connections\n4. Impact tracking\n5. Recognition program\nStart donating!",
                "Being a donor means:\n1. Listing food\n2. Scheduling pickups\n3. Helping community\n4. Tracking impact\n5. Getting rewards\nReady to join?"
            ],
            
            # Collector
            'collector': [
                "As a collector, you can:\n1. Find food listings\n2. Claim items\n3. Schedule pickups\n4. Help distribute\n5. Track collections\nRegister as a collector to start!",
                "Collectors help by:\n1. Browsing listings\n2. Claiming food\n3. Arranging pickups\n4. Distributing food\n5. Building networks\nJoin as a collector today!",
                "Collectors are vital! You can:\n1. Search listings\n2. Get food items\n3. Plan pickups\n4. Help others\n5. Track progress\nBecome a collector now!",
                "As a collector, you'll:\n1. Browse food listings\n2. Claim items\n3. Schedule pickups\n4. Distribute food\n5. Track collections\nStart collecting today!",
                "Collectors can:\n1. Find food items\n2. Arrange pickups\n3. Help distribute\n4. Build networks\n5. Track impact\nJoin as a collector now!",
                "Being a collector means:\n1. Finding food\n2. Claiming items\n3. Scheduling pickups\n4. Helping others\n5. Tracking collections\nReady to start?",
                "Collectors have access to:\n1. Food listings\n2. Pickup scheduling\n3. Distribution tools\n4. Network building\n5. Impact tracking\nBecome a collector today!",
                "As a collector, you get to:\n1. Browse listings\n2. Claim food\n3. Schedule pickups\n4. Help distribute\n5. Track impact\nJoin us now!",
                "Collectors can enjoy:\n1. Food listings\n2. Easy pickups\n3. Distribution help\n4. Network building\n5. Impact tracking\nStart collecting!",
                "Being a collector means:\n1. Finding food\n2. Claiming items\n3. Helping others\n4. Building networks\n5. Tracking impact\nReady to join?"
            ],
            
            # Safety
            'safety': [
                "Food safety guidelines:\n1. Check expiry dates\n2. Proper packaging\n3. Temperature control\n4. Clean handling\n5. Safe storage\n6. Clear labeling",
                "Keep food safe with:\n1. Date verification\n2. Good packaging\n3. Temp monitoring\n4. Hygiene practices\n5. Proper storage\n6. Clear labels",
                "Safety tips:\n1. Verify dates\n2. Package well\n3. Control temperature\n4. Stay clean\n5. Store properly\n6. Label clearly",
                "Food safety rules:\n1. Check dates\n2. Package properly\n3. Monitor temperature\n4. Maintain hygiene\n5. Store safely\n6. Label items",
                "Safety guidelines:\n1. Verify expiry\n2. Package correctly\n3. Control temp\n4. Keep clean\n5. Store well\n6. Label clearly",
                "Food safety tips:\n1. Check dates\n2. Package items\n3. Monitor temp\n4. Stay hygienic\n5. Store safely\n6. Label properly",
                "Safety measures:\n1. Date checking\n2. Proper packaging\n3. Temp control\n4. Clean handling\n5. Safe storage\n6. Clear labeling",
                "Food safety steps:\n1. Verify dates\n2. Package well\n3. Control temp\n4. Stay clean\n5. Store safely\n6. Label items",
                "Safety protocols:\n1. Check expiry\n2. Package properly\n3. Monitor temp\n4. Maintain hygiene\n5. Store safely\n6. Label clearly",
                "Food safety rules:\n1. Verify dates\n2. Package items\n3. Control temp\n4. Keep clean\n5. Store well\n6. Label properly"
            ],
            
            # Account
            'account': [
                "Account management:\n1. Access profile\n2. Edit details\n3. Update info\n4. Set preferences\n5. View history\n6. Manage listings",
                "Manage your account:\n1. Open profile\n2. Change details\n3. Update settings\n4. Set options\n5. Check history\n6. Handle listings",
                "Account features:\n1. Profile access\n2. Edit information\n3. Update settings\n4. Set preferences\n5. View activity\n6. Manage posts",
                "Account options:\n1. View profile\n2. Edit details\n3. Update settings\n4. Set preferences\n5. Check history\n6. Manage listings",
                "Account tools:\n1. Access profile\n2. Modify details\n3. Update info\n4. Set options\n5. View history\n6. Handle posts",
                "Account settings:\n1. Profile management\n2. Edit information\n3. Update details\n4. Set preferences\n5. View history\n6. Manage listings",
                "Account features:\n1. Profile access\n2. Edit details\n3. Update settings\n4. Set options\n5. View history\n6. Manage posts",
                "Account management:\n1. Access profile\n2. Edit information\n3. Update settings\n4. Set preferences\n5. View history\n6. Handle listings",
                "Account options:\n1. View profile\n2. Edit details\n3. Update settings\n4. Set preferences\n5. Check history\n6. Manage posts",
                "Account tools:\n1. Access profile\n2. Modify information\n3. Update settings\n4. Set options\n5. View history\n6. Handle listings"
            ],
            
            # Food Types
            'food': [
                "You can donate/collect:\n1. Fresh produce\n2. Packaged goods\n3. Baked items\n4. Dairy products\n5. Frozen foods\n6. Non-perishables",
                "Acceptable items:\n1. Fruits & vegetables\n2. Canned goods\n3. Bread & pastries\n4. Dairy items\n5. Frozen products\n6. Long-lasting items",
                "Food categories:\n1. Fresh produce\n2. Packaged foods\n3. Baked goods\n4. Dairy items\n5. Frozen items\n6. Non-perishables",
                "Food types:\n1. Fresh produce\n2. Packaged items\n3. Baked goods\n4. Dairy products\n5. Frozen foods\n6. Non-perishables",
                "Acceptable foods:\n1. Fruits & veggies\n2. Canned items\n3. Bread & pastries\n4. Dairy products\n5. Frozen goods\n6. Long-lasting items",
                "Food categories:\n1. Fresh produce\n2. Packaged goods\n3. Baked items\n4. Dairy products\n5. Frozen foods\n6. Non-perishables",
                "Food types:\n1. Fresh produce\n2. Packaged items\n3. Baked goods\n4. Dairy products\n5. Frozen foods\n6. Non-perishables",
                "Acceptable items:\n1. Fruits & vegetables\n2. Canned goods\n3. Bread & pastries\n4. Dairy items\n5. Frozen products\n6. Long-lasting items",
                "Food categories:\n1. Fresh produce\n2. Packaged foods\n3. Baked goods\n4. Dairy items\n5. Frozen items\n6. Non-perishables",
                "Food types:\n1. Fresh produce\n2. Packaged items\n3. Baked goods\n4. Dairy products\n5. Frozen foods\n6. Non-perishables"
            ],
            
            # Location
            'location': [
                "Location features:\n1. Add locations\n2. Find nearby users\n3. Set pickup points\n4. View distances\n5. Get directions\n6. Set zones",
                "Location options:\n1. List locations\n2. Search nearby\n3. Choose pickups\n4. Check distance\n5. Get navigation\n6. Define areas",
                "Location tools:\n1. Set locations\n2. Find users\n3. Pickup spots\n4. Distance view\n5. Directions\n6. Zone setup",
                "Location features:\n1. Add places\n2. Find users\n3. Set pickups\n4. View distances\n5. Get directions\n6. Set zones",
                "Location options:\n1. List places\n2. Search users\n3. Choose pickups\n4. Check distance\n5. Get navigation\n6. Define areas",
                "Location tools:\n1. Set places\n2. Find users\n3. Pickup spots\n4. Distance view\n5. Directions\n6. Zone setup",
                "Location features:\n1. Add locations\n2. Find nearby\n3. Set pickups\n4. View distances\n5. Get directions\n6. Set zones",
                "Location options:\n1. List locations\n2. Search nearby\n3. Choose pickups\n4. Check distance\n5. Get navigation\n6. Define areas",
                "Location tools:\n1. Set locations\n2. Find users\n3. Pickup spots\n4. Distance view\n5. Directions\n6. Zone setup",
                "Location features:\n1. Add places\n2. Find users\n3. Set pickups\n4. View distances\n5. Get directions\n6. Set zones"
            ],
            
            # Time
            'time': [
                "Time management:\n1. Set pickup times\n2. Schedule ahead\n3. Coordinate timing\n4. Set availability\n5. Get alerts\n6. View calendar",
                "Schedule options:\n1. Choose times\n2. Plan pickups\n3. Coordinate\n4. Set hours\n5. Get notifications\n6. Check schedule",
                "Time features:\n1. Pickup scheduling\n2. Advance booking\n3. Time coordination\n4. Availability\n5. Alerts\n6. Calendar",
                "Time management:\n1. Set pickups\n2. Schedule ahead\n3. Coordinate times\n4. Set availability\n5. Get alerts\n6. View calendar",
                "Schedule options:\n1. Choose pickups\n2. Plan ahead\n3. Coordinate times\n4. Set hours\n5. Get notifications\n6. Check schedule",
                "Time features:\n1. Pickup scheduling\n2. Advance booking\n3. Time coordination\n4. Availability\n5. Alerts\n6. Calendar",
                "Time management:\n1. Set pickups\n2. Schedule ahead\n3. Coordinate times\n4. Set availability\n5. Get alerts\n6. View calendar",
                "Schedule options:\n1. Choose pickups\n2. Plan ahead\n3. Coordinate times\n4. Set hours\n5. Get notifications\n6. Check schedule",
                "Time features:\n1. Pickup scheduling\n2. Advance booking\n3. Time coordination\n4. Availability\n5. Alerts\n6. Calendar",
                "Time management:\n1. Set pickups\n2. Schedule ahead\n3. Coordinate times\n4. Set availability\n5. Get alerts\n6. View calendar"
            ],
            
            # Benefits
            'benefits': [
                "Benefits of EcoByte:\n1. Reduce waste\n2. Help others\n3. Community\n4. Make impact\n5. Save resources\n6. Build connections",
                "Why choose EcoByte:\n1. Cut waste\n2. Support others\n3. Connect community\n4. Create change\n5. Save resources\n6. Build networks",
                "EcoByte advantages:\n1. Waste reduction\n2. Helping others\n3. Community ties\n4. Making impact\n5. Resource saving\n6. Building connections",
                "Benefits of EcoByte:\n1. Reduce waste\n2. Help others\n3. Community\n4. Make impact\n5. Save resources\n6. Build connections",
                "Why choose EcoByte:\n1. Cut waste\n2. Support others\n3. Connect community\n4. Create change\n5. Save resources\n6. Build networks",
                "EcoByte advantages:\n1. Waste reduction\n2. Helping others\n3. Community ties\n4. Making impact\n5. Resource saving\n6. Building connections",
                "Benefits of EcoByte:\n1. Reduce waste\n2. Help others\n3. Community\n4. Make impact\n5. Save resources\n6. Build connections",
                "Why choose EcoByte:\n1. Cut waste\n2. Support others\n3. Connect community\n4. Create change\n5. Save resources\n6. Build networks",
                "EcoByte advantages:\n1. Waste reduction\n2. Helping others\n3. Community ties\n4. Making impact\n5. Resource saving\n6. Building connections",
                "Benefits of EcoByte:\n1. Reduce waste\n2. Help others\n3. Community\n4. Make impact\n5. Save resources\n6. Build connections"
            ],
            
            # Registration
            'register': [
                "To register:\n1. Click Register\n2. Fill details\n3. Choose role\n4. Verify email\n5. Start helping!",
                "Registration steps:\n1. Hit Register\n2. Enter info\n3. Select role\n4. Verify email\n5. Begin!",
                "Join EcoByte:\n1. Press Register\n2. Add details\n3. Pick role\n4. Verify email\n5. Get started!",
                "Registration process:\n1. Click Register\n2. Fill details\n3. Choose role\n4. Verify email\n5. Start helping!",
                "Sign up steps:\n1. Hit Register\n2. Enter info\n3. Select role\n4. Verify email\n5. Begin!",
                "Join process:\n1. Press Register\n2. Add details\n3. Pick role\n4. Verify email\n5. Get started!",
                "Registration guide:\n1. Click Register\n2. Fill details\n3. Choose role\n4. Verify email\n5. Start helping!",
                "Sign up guide:\n1. Hit Register\n2. Enter info\n3. Select role\n4. Verify email\n5. Begin!",
                "Join guide:\n1. Press Register\n2. Add details\n3. Pick role\n4. Verify email\n5. Get started!",
                "Registration steps:\n1. Click Register\n2. Fill details\n3. Choose role\n4. Verify email\n5. Start helping!"
            ],
            
            # Login
            'login': [
                "To login:\n1. Click Login\n2. Enter credentials\n3. Press Login\nNeed help? Click 'Forgot Password'",
                "Login steps:\n1. Press Login\n2. Type details\n3. Click Enter\nForgot password? Use 'Forgot Password'",
                "Access account:\n1. Select Login\n2. Input details\n3. Click Login\nNeed password help? Click 'Forgot Password'",
                "Login process:\n1. Click Login\n2. Enter credentials\n3. Press Login\nNeed help? Click 'Forgot Password'",
                "Sign in steps:\n1. Press Login\n2. Type details\n3. Click Enter\nForgot password? Use 'Forgot Password'",
                "Access steps:\n1. Select Login\n2. Input details\n3. Click Login\nNeed password help? Click 'Forgot Password'",
                "Login guide:\n1. Click Login\n2. Enter credentials\n3. Press Login\nNeed help? Click 'Forgot Password'",
                "Sign in guide:\n1. Press Login\n2. Type details\n3. Click Enter\nForgot password? Use 'Forgot Password'",
                "Access guide:\n1. Select Login\n2. Input details\n3. Click Login\nNeed password help? Click 'Forgot Password'",
                "Login steps:\n1. Click Login\n2. Enter credentials\n3. Press Login\nNeed help? Click 'Forgot Password'"
            ],
            
            # Contact
            'contact': [
                "Contact us:\n1. Email: support@ecobyte.com\n2. Phone: (555) 123-4567\n3. Live chat\n4. Social media",
                "Reach us at:\n1. support@ecobyte.com\n2. (555) 123-4567\n3. Live chat\n4. Social platforms",
                "Get in touch:\n1. Email support\n2. Call us\n3. Live chat\n4. Social media",
                "Contact options:\n1. Email: support@ecobyte.com\n2. Phone: (555) 123-4567\n3. Live chat\n4. Social media",
                "Reach out to:\n1. support@ecobyte.com\n2. (555) 123-4567\n3. Live chat\n4. Social platforms",
                "Contact details:\n1. Email support\n2. Call us\n3. Live chat\n4. Social media",
                "Contact information:\n1. Email: support@ecobyte.com\n2. Phone: (555) 123-4567\n3. Live chat\n4. Social media",
                "Reach us through:\n1. support@ecobyte.com\n2. (555) 123-4567\n3. Live chat\n4. Social platforms",
                "Get in touch via:\n1. Email support\n2. Call us\n3. Live chat\n4. Social media",
                "Contact us at:\n1. Email: support@ecobyte.com\n2. Phone: (555) 123-4567\n3. Live chat\n4. Social media"
            ],
            
            # Default
            'default': [
                "I can help with:\n1. Food donation\n2. Collection\n3. Safety\n4. Account\n5. Registration\nType 'help' for more!",
                "Let me guide you:\n1. Donation\n2. Collection\n3. Safety\n4. Account\n5. Sign up\nNeed more? Type 'help'",
                "I can assist with:\n1. Donating\n2. Collecting\n3. Safety\n4. Account\n5. Registration\nWant more? Type 'help'",
                "I can help with:\n1. Food donation\n2. Collection\n3. Safety\n4. Account\n5. Registration\nType 'help' for more!",
                "Let me guide you:\n1. Donation\n2. Collection\n3. Safety\n4. Account\n5. Sign up\nNeed more? Type 'help'",
                "I can assist with:\n1. Donating\n2. Collecting\n3. Safety\n4. Account\n5. Registration\nWant more? Type 'help'",
                "I can help with:\n1. Food donation\n2. Collection\n3. Safety\n4. Account\n5. Registration\nType 'help' for more!",
                "Let me guide you:\n1. Donation\n2. Collection\n3. Safety\n4. Account\n5. Sign up\nNeed more? Type 'help'",
                "I can assist with:\n1. Donating\n2. Collecting\n3. Safety\n4. Account\n5. Registration\nWant more? Type 'help'",
                "I can help with:\n1. Food donation\n2. Collection\n3. Safety\n4. Account\n5. Registration\nType 'help' for more!"
            ]
        }
        
        # Patterns for matching
        self.patterns = {
            'greeting': r'\b(hi|hello|hey|greetings|sup|yo|good\s*(morning|afternoon|evening)|welcome|hiya|howdy|hola|namaste|bonjour|ciao|hallo|konnichiwa)\b',
            'help': r'\b(help|support|assist|guide|what\s*can\s*you\s*do|how\s*can\s*you\s*help|what\s*do\s*you\s*do|how\s*does\s*this\s*work|what\s*are\s*you\s*for)\b',
            'donor': r'\b(donor|donate|donating|donation|give\s*food|share\s*food|provide\s*food|offer\s*food|contribute\s*food|hand\s*out\s*food)\b',
            'collector': r'\b(collector|collect|collecting|pickup|get\s*food|receive\s*food|take\s*food|gather\s*food|obtain\s*food|acquire\s*food)\b',
            'safety': r'\b(safety|safe|hygiene|quality|food\s*safety|food\s*quality|health|clean|sanitary|sterile|hygienic|quality\s*control)\b',
            'account': r'\b(account|profile|settings|manage|my\s*account|user\s*profile|dashboard|control\s*panel|user\s*settings|account\s*management)\b',
            'food': r'\b(food|items|products|groceries|what\s*can\s*i\s*(donate|collect)|edibles|provisions|supplies|produce|ingredients|meals)\b',
            'location': r'\b(location|where|place|address|pickup\s*location|drop\s*off|venue|site|spot|area|zone|region|district)\b',
            'time': r'\b(time|when|schedule|pickup\s*time|availability|when\s*can\s*i|timing|period|duration|moment|hour|date|day)\b',
            'benefits': r'\b(benefit|advantage|why|purpose|why\s*should\s*i|perk|pro|plus|upside|merit|value|worth|gain|profit)\b',
            'register': r'\b(register|signup|sign\s*up|create\s*account|join|become\s*a\s*(donor|collector)|enroll|enlist|sign\s*on|sign\s*in|get\s*started)\b',
            'login': r'\b(login|signin|sign\s*in|log\s*in|access\s*account|enter|get\s*in|access|connect|authenticate|verify|validate)\b',
            'contact': r'\b(contact|support|help|reach|email|phone|get\s*in\s*touch|message|call|text|write|communicate|connect|reach\s*out)\b'
        }

    def get_response(self, message, user=None):
        try:
            # Convert message to lowercase and strip whitespace
            message = message.lower().strip()
            logger.info(f"Processing message: {message}")
            
            # Check each pattern
            for category, pattern in self.patterns.items():
                if re.search(pattern, message):
                    logger.info(f"Matched category: {category}")
                    return random.choice(self.responses[category])
            
            # If no pattern matches, return default response
            logger.info("No pattern match, using default response")
            return random.choice(self.responses['default'])
            
        except Exception as e:
            logger.error(f"Error in get_response: {e}")
            return random.choice(self.responses['default'])

# Create a single instance of the chatbot
chatbot = ChatBot()

@login_required
def chat_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            if not user_message:
                return JsonResponse({
                    'response': "Please enter a message."
                })
            
            # Save user message
            ChatMessage.objects.create(
                user=request.user,
                message=user_message,
                is_bot=False
            )
            
            # Get bot response
            bot_response = chatbot.get_response(user_message, request.user)
            
            # Save bot response
            ChatMessage.objects.create(
                user=request.user,
                message=bot_response,
                is_bot=True
            )
            
            return JsonResponse({
                'response': bot_response
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'response': "I couldn't understand your message. Please try again."
            })
        except Exception as e:
            logger.error(f"Error in chat_view: {e}")
            return JsonResponse({
                'response': random.choice([
                    "I can help with:\n1. Food donation\n2. Collection\n3. Safety\n4. Account\n5. Registration\nType 'help' for more!",
                    "Let me guide you:\n1. Donation\n2. Collection\n3. Safety\n4. Account\n5. Sign up\nNeed more? Type 'help'",
                    "I can assist with:\n1. Donating\n2. Collecting\n3. Safety\n4. Account\n5. Registration\nWant more? Type 'help'"
                ])
            })
    
    # Get chat history for the user
    chat_history = ChatMessage.objects.filter(user=request.user).order_by('created_at')
    
    # If it's an AJAX request, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'chat_history': list(chat_history.values('message', 'is_bot', 'created_at'))
        })
    
    # Otherwise, render the full chat page
    return render(request, 'chatbot/chat.html', {
        'chat_history': chat_history
    })
