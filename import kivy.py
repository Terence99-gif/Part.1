import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.lang import Builder # Import Builder

# --- Define the Kivy Language String ---
# This string contains the entire content of the previous khuthaza.kv file
KV_STRING = """
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import dp kivy.metrics.dp

# Define colors globally for use in kv
#:set COLOR_PRIMARY get_color_from_hex('#007bff')
#:set COLOR_SECONDARY get_color_from_hex('#ffc107')
#:set COLOR_ACCENT get_color_from_hex('#6c757d')
#:set COLOR_SUCCESS get_color_from_hex('#28a745')
#:set COLOR_DANGER get_color_from_hex('#dc3545')
#:set COLOR_BACKGROUND get_color_from_hex('#f8f9fa')
#:set COLOR_TEXT get_color_from_hex('#212529')
#:set COLOR_WHITE get_color_from_hex('#ffffff')

# --- Screen Manager Root Widget ---
# Define the root widget directly here if needed, or rely on the App class build method
KhuthazaAppManager:
    # Screens will be added dynamically in the Python build method
    # MapScreen: # No longer need to define them here if added in build()
    # RankListScreen:
    # RankDetailScreen:
    # MyRoutesScreen:
    # SettingsScreen:

# --- Widget Styles (Applied globally) ---
<Screen>:
    canvas.before:
        Color:
            rgba: COLOR_BACKGROUND
        Rectangle:
            pos: self.pos
            size: self.size

<Label>:
    color: COLOR_TEXT
    font_size: '16sp' # Default font size

<Button>:
    font_size: '16sp'
    background_normal: '' # Allows background_color to work
    background_color: COLOR_PRIMARY
    color: COLOR_WHITE
    size_hint_y: None
    height: dp(48)

<TextInput>:
    font_size: '16sp'
    padding: [dp(10), dp(10), dp(10), dp(10)] # top, right, bottom, left padding inside textinput
    size_hint_y: None
    height: dp(44)
    background_color: COLOR_WHITE
    color: COLOR_TEXT
    hint_text_color: COLOR_ACCENT

# --- Custom Reusable Label Styles ---
<TitleLabel@Label>:
    font_size: '24sp'
    bold: True
    size_hint_y: None
    height: dp(50)
    color: COLOR_PRIMARY
    halign: 'center'

<SubTitleLabel@Label>:
    font_size: '18sp'
    bold: True
    size_hint_y: None
    height: dp(40)
    color: COLOR_TEXT
    padding: (dp(10), dp(5))

<BodyLabel@Label>:
    font_size: '15sp'
    color: COLOR_ACCENT
    size_hint_y: None
    height: dp(30)
    padding: (dp(10), dp(5))

# --- Screen Layout Definitions ---

<MapScreen>:
    name: 'map'
    BoxLayout:
        orientation: 'vertical'
        TitleLabel:
            text: "Khuthaza Map"
        BoxLayout:
            id: map_placeholder_box
            size_hint_y: 0.8 # Take up most space
            # Placeholder Label added in Python
        BoxLayout: # Bottom Navigation
            size_hint_y: None
            height: dp(55)
            Button:
                text: "Map"
                background_color: COLOR_SECONDARY if root.manager.current == 'map' else COLOR_PRIMARY # Highlight current
                on_release: app.go_to_map()
            Button:
                text: "Ranks"
                background_color: COLOR_SECONDARY if root.manager.current == 'rank_list' else COLOR_PRIMARY
                on_release: app.go_to_rank_list()
            Button:
                text: "Routes"
                background_color: COLOR_SECONDARY if root.manager.current == 'my_routes' else COLOR_PRIMARY
                on_release: app.go_to_my_routes()
            Button:
                text: "Settings"
                background_color: COLOR_SECONDARY if root.manager.current == 'settings' else COLOR_PRIMARY
                on_release: app.go_to_settings()

<RankListScreen>:
    name: 'rank_list'
    BoxLayout:
        orientation: 'vertical'
        TitleLabel:
            text: "Find Taxi Ranks"
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            padding: dp(10)
            spacing: dp(10)
            TextInput:
                id: search_input
                hint_text: "Search by rank name or destination..."
                size_hint_x: 0.8
                multiline: False
                on_text_validate: root.search_ranks() # Search on pressing Enter
            Button:
                text: "Search"
                size_hint_x: 0.2
                on_release: root.search_ranks()
        ScrollView:
            size_hint_y: 0.8
            do_scroll_x: False
            bar_width: dp(10) # Make scrollbar visible
            GridLayout:
                id: rank_list_layout
                cols: 1
                size_hint_y: None
                spacing: dp(5)
                padding: dp(10)
                # This binding makes the GridLayout height fit its content
                bind: minimum_height=self.setter('height')
                # RankListItem widgets added dynamically via Python
        BoxLayout: # Bottom Navigation
            size_hint_y: None
            height: dp(55)
            Button:
                text: "Map"
                background_color: COLOR_SECONDARY if root.manager.current == 'map' else COLOR_PRIMARY
                on_release: app.go_to_map()
            Button:
                text: "Ranks"
                background_color: COLOR_SECONDARY if root.manager.current == 'rank_list' else COLOR_PRIMARY
                on_release: app.go_to_rank_list()
            Button:
                text: "Routes"
                background_color: COLOR_SECONDARY if root.manager.current == 'my_routes' else COLOR_PRIMARY
                on_release: app.go_to_my_routes()
            Button:
                text: "Settings"
                background_color: COLOR_SECONDARY if root.manager.current == 'settings' else COLOR_PRIMARY
                on_release: app.go_to_settings()


<RankDetailScreen>:
    name: 'rank_detail'
    BoxLayout:
        orientation: 'vertical'
        BoxLayout: # Header with Back Button
            size_hint_y: None
            height: dp(50)
            Button:
                text: "< Back"
                size_hint_x: 0.25
                background_color: COLOR_ACCENT
                on_release: root.go_back() # Use the method defined in Python class
            Label:
                id: rank_name_label
                text: "Rank Name Placeholder"
                font_size: '20sp'
                bold: True
                size_hint_x: 0.75
                halign: 'center'
                valign: 'middle'
        SubTitleLabel:
            text: "Destinations & Availability:"
            halign: 'left'
            padding: (dp(10), dp(10))
        ScrollView:
            size_hint_y: 0.6
            do_scroll_x: False
            bar_width: dp(10)
            GridLayout:
                id: destinations_layout
                cols: 1
                size_hint_y: None
                spacing: dp(2)
                padding: (dp(10), dp(5))
                # Height binding set in Python
                # Destination items added dynamically
        BodyLabel:
            id: timestamp_label
            text: "Last report: loading..."
            halign: 'left'
            padding: (dp(10), dp(10))
        BoxLayout: # Action Buttons Area
            orientation: 'vertical'
            padding: dp(15)
            spacing: dp(10)
            size_hint_y: None
            height: dp(130) # Adjust as needed
            Button:
                text: "Report Availability Here"
                background_color: COLOR_SECONDARY
                color: COLOR_TEXT # Yellow needs dark text
                on_release: root.report_availability()
            Button:
                text: "Add to My Routes" # Placeholder action
                background_color: COLOR_PRIMARY
                # on_release: root.add_to_routes() # Implement this method later


<MyRoutesScreen>:
    name: 'my_routes'
    BoxLayout:
        orientation: 'vertical'
        TitleLabel:
            text: "My Routes"
        Button:
            text: "+ Add New Route"
            size_hint_y: None
            height: dp(45)
            background_color: COLOR_SUCCESS
            on_release: root.add_route() # Use method from Python class
            # Add margin/padding if needed (can be done via BoxLayout parent)
            # margin: [dp(10), dp(5)] # Example if it were in another layout
        ScrollView:
            size_hint_y: 0.8
            do_scroll_x: False
            bar_width: dp(10)
            GridLayout:
                id: routes_layout
                cols: 1
                size_hint_y: None
                spacing: dp(5)
                padding: dp(10)
                # Height binding set in Python
                # RouteListItem widgets added dynamically
        BoxLayout: # Bottom Navigation
            size_hint_y: None
            height: dp(55)
            Button:
                text: "Map"
                background_color: COLOR_SECONDARY if root.manager.current == 'map' else COLOR_PRIMARY
                on_release: app.go_to_map()
            Button:
                text: "Ranks"
                background_color: COLOR_SECONDARY if root.manager.current == 'rank_list' else COLOR_PRIMARY
                on_release: app.go_to_rank_list()
            Button:
                text: "Routes"
                background_color: COLOR_SECONDARY if root.manager.current == 'my_routes' else COLOR_PRIMARY
                on_release: app.go_to_my_routes()
            Button:
                text: "Settings"
                background_color: COLOR_SECONDARY if root.manager.current == 'settings' else COLOR_PRIMARY
                on_release: app.go_to_settings()


<SettingsScreen>:
    name: 'settings'
    BoxLayout:
        orientation: 'vertical'
        TitleLabel:
            text: "Settings & Safety"
        ScrollView:
            size_hint_y: 0.8
            bar_width: dp(10)
            GridLayout:
                cols: 1
                size_hint_y: None
                height: self.minimum_height # Make layout scrollable
                padding: dp(15)
                spacing: dp(15)

                Button:
                    text: "SOS / Emergency Alert"
                    background_color: COLOR_DANGER
                    on_release: root.trigger_sos()
                Button:
                    text: "Share My Journey"
                    background_color: COLOR_SECONDARY
                    color: COLOR_TEXT
                    on_release: root.share_journey()
                Button:
                    text: "Manage Profile"
                    background_color: COLOR_ACCENT
                    on_release: root.manage_profile()
                Button:
                    text: "Notification Alerts"
                    background_color: COLOR_ACCENT
                    on_release: root.manage_alerts()
                Button:
                    text: "Emergency Contacts"
                    background_color: COLOR_ACCENT
                    on_release: root.manage_emergency_contacts()
                # Add Driver Mode switch later if needed
                # Add Logout, About, etc.

        BoxLayout: # Bottom Navigation
            size_hint_y: None
            height: dp(55)
            Button:
                text: "Map"
                background_color: COLOR_SECONDARY if root.manager.current == 'map' else COLOR_PRIMARY
                on_release: app.go_to_map()
            Button:
                text: "Ranks"
                background_color: COLOR_SECONDARY if root.manager.current == 'rank_list' else COLOR_PRIMARY
                on_release: app.go_to_rank_list()
            Button:
                text: "Routes"
                background_color: COLOR_SECONDARY if root.manager.current == 'my_routes' else COLOR_PRIMARY
                on_release: app.go_to_my_routes()
            Button:
                text: "Settings"
                background_color: COLOR_SECONDARY if root.manager.current == 'settings' else COLOR_PRIMARY
                on_release: app.go_to_settings()
"""

# --- Python Code (Logic and Classes) ---

# Define our colors (Python variables, can be used in Python code)
COLOR_PRIMARY_PY = get_color_from_hex('#007bff') # Blue
COLOR_SECONDARY_PY = get_color_from_hex('#ffc107') # Yellow
COLOR_ACCENT_PY = get_color_from_hex('#6c757d') # Grey
COLOR_SUCCESS_PY = get_color_from_hex('#28a745') # Green
COLOR_DANGER_PY = get_color_from_hex('#dc3545') # Red
COLOR_BACKGROUND_PY = get_color_from_hex('#f8f9fa') # Light Grey
COLOR_TEXT_PY = get_color_from_hex('#212529') # Dark Grey/Black
COLOR_WHITE_PY = get_color_from_hex('#ffffff')

Window.clearcolor = COLOR_BACKGROUND_PY

# --- Dummy Data ---
TAXI_RANKS = {
    "rank_001": {"name": "Bosman Street Station", "destinations": {"Menlyn": "Plenty", "Sunnyside": "Waiting", "Centurion": "Few"}, "coords": (-25.750, 28.185)},
    "rank_002": {"name": "Bloed Street Mall", "destinations": {"Pretoria North": "Plenty", "Mamelodi": "Plenty", "Atteridgeville": "Waiting"}, "coords": (-25.742, 28.190)},
    "rank_003": {"name": "Menlyn Park", "destinations": {"Hatfield": "Waiting", "Brooklyn": "Few", "City Centre": "Plenty"}, "coords": (-25.782, 28.275)},
    "rank_004": {"name": "Centurion Mall", "destinations": {"Midrand": "Plenty", "Irene": "Waiting", "City Centre": "Waiting"}, "coords": (-25.860, 28.186)},
}

MY_ROUTES_DATA = [
    {"origin": "Bosman Street Station", "destination": "Menlyn", "status": "Plenty"},
    {"origin": "Bloed Street Mall", "destination": "Mamelodi", "status": "Plenty"},
]

# --- Custom Widgets (Python Classes) ---

class RankListItem(BoxLayout):
    rank_id = StringProperty('')
    rank_name = StringProperty('')

    def __init__(self, rank_id, rank_name, **kwargs):
        super().__init__(**kwargs)
        # Basic styling in Python (more complex styling better in KV)
        self.orientation = 'horizontal' # Changed to horizontal to contain button
        self.size_hint_y = None
        self.height = dp(60)
        self.padding = dp(5)

        self.rank_id = rank_id
        self.rank_name = rank_name

        # Use a Button for the whole item to make it tappable
        item_button = Button(
            text=self.rank_name,
            color=COLOR_TEXT_PY,
            halign='left',
            valign='middle',
            size_hint=(1, 1),
            text_size=(Window.width - dp(40), None), # Adjust width for padding
            background_color=(0,0,0,0), # Transparent background
            background_normal='',
            on_release=self.go_to_details
        )
        item_button.bind(size=item_button.setter('text_size')) # Update text_size on resize

        self.add_widget(item_button)

    def go_to_details(self, instance):
        app = App.get_running_app()
        # Check if the screen exists before switching
        if 'rank_detail' in app.root.screen_names:
            app.root.current = 'rank_detail'
            # Ensure the screen instance is retrieved correctly
            detail_screen = app.root.get_screen('rank_detail')
            detail_screen.load_rank_data(self.rank_id)
        else:
            print(f"Error: Screen 'rank_detail' not found in ScreenManager.")


class RouteListItem(BoxLayout):
     def __init__(self, origin, destination, status, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = dp(10)
        self.spacing = dp(10)

        status_color = COLOR_SUCCESS_PY if status == "Plenty" else (COLOR_SECONDARY_PY if status == "Waiting" else COLOR_DANGER_PY)

        self.add_widget(Label(text=f"{origin} -> {destination}", color=COLOR_TEXT_PY, size_hint_x=0.7, halign='left', text_size=(self.width*0.6, None)))
        self.add_widget(Label(text=status, color=status_color, size_hint_x=0.3, bold=True, halign='right', text_size=(self.width*0.25, None)))
        self.bind(size=self._update_text_sizes) # Update text sizes if layout resizes

     def _update_text_sizes(self, instance, value):
        # Simple text size update on resize
        if len(self.children) == 2:
            self.children[1].text_size = (self.width * 0.6, None) # Label 1 (route)
            self.children[0].text_size = (self.width * 0.25, None) # Label 2 (status)

# --- Screens (Python Classes) ---

class MapScreen(Screen):
    def on_enter(self, *args):
        # Placeholder: In a real app, initialize map view here
        map_placeholder = self.ids.map_placeholder_box
        map_placeholder.clear_widgets() # Clear previous widgets if any
        map_placeholder.add_widget(Label(text="[Map View Placeholder]\n\n(Requires separate map library\nlike kivy_garden.mapview)", halign='center', color=COLOR_ACCENT_PY))
        # Add dummy markers (simple buttons for now)
        # Note: Positioning these accurately without a real map widget is hard.
        # This is just a visual representation.
        marker_layout = BoxLayout(orientation='vertical', spacing=dp(5), padding=dp(10))
        for rank_id, data in TAXI_RANKS.items():
             marker_btn = Button(
                 text=data['name'],
                 size_hint=(1, None), # Take full width in this dummy layout
                 height=dp(40),
                 background_color=COLOR_PRIMARY_PY,
                 on_release=lambda btn, r_id=rank_id: self.view_rank_details(r_id)
                 )
             marker_layout.add_widget(marker_btn)
        map_placeholder.add_widget(marker_layout)

    def view_rank_details(self, rank_id):
        app = App.get_running_app()
        if 'rank_detail' in app.root.screen_names:
            app.root.current = 'rank_detail'
            app.root.get_screen('rank_detail').load_rank_data(rank_id)
        else:
             print(f"Error: Screen 'rank_detail' not found.")


class RankListScreen(Screen):
    def on_enter(self, *args):
        # Load initial list when screen is entered
        if not self.ids.rank_list_layout.children: # Avoid reloading if already populated
             self.update_rank_list()

    def update_rank_list(self, search_term=""):
        rank_list_layout = self.ids.rank_list_layout
        rank_list_layout.clear_widgets() # Clear previous list
        search_term = search_term.strip().lower()

        found = False
        for rank_id, data in TAXI_RANKS.items():
            # Search in name or destinations
            match_name = search_term in data['name'].lower()
            match_dest = any(search_term in dest.lower() for dest in data['destinations'])

            if not search_term or match_name or match_dest:
                 item = RankListItem(rank_id=rank_id, rank_name=data['name'])
                 rank_list_layout.add_widget(item)
                 found = True

        if not found and search_term:
             rank_list_layout.add_widget(Label(text="No ranks match your search.", size_hint_y=None, height=dp(40), color=COLOR_ACCENT_PY))
        elif not found and not search_term:
             rank_list_layout.add_widget(Label(text="No ranks available (check data).", size_hint_y=None, height=dp(40), color=COLOR_ACCENT_PY))


    def search_ranks(self):
        search_input = self.ids.search_input
        self.update_rank_list(search_input.text)


class RankDetailScreen(Screen):
    rank_id = StringProperty('') # Keep track of the current rank

    def load_rank_data(self, rank_id):
        self.rank_id = rank_id
        if rank_id in TAXI_RANKS:
            data = TAXI_RANKS[rank_id]
            self.ids.rank_name_label.text = data['name']

            dest_layout = self.ids.destinations_layout
            dest_layout.clear_widgets() # Clear previous destinations
            # Bind minimum_height for ScrollView compatibility - already done in KV

            if data['destinations']:
                for dest, status in data['destinations'].items():
                     status_color = COLOR_SUCCESS_PY if status == "Plenty" else (COLOR_SECONDARY_PY if status == "Waiting" else COLOR_DANGER_PY)
                     item = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), padding=(dp(10), 0))
                     # Use text_size for wrapping within the layout constraints
                     item.add_widget(Label(text=dest, color=COLOR_TEXT_PY, size_hint_x=0.6, halign='left', valign='middle', text_size=(self.width*0.5, None)))
                     item.add_widget(Label(text=status, color=status_color, size_hint_x=0.4, bold=True, halign='right', valign='middle', text_size=(self.width*0.3, None)))
                     dest_layout.add_widget(item)
            else:
                 dest_layout.add_widget(Label(text="No destinations listed.", color=COLOR_ACCENT_PY, size_hint_y=None, height=dp(40)))

            # Add timestamp (dummy)
            self.ids.timestamp_label.text = "Last report: Just now (Simulated)" # Replace with real logic
        else:
            self.ids.rank_name_label.text = "Rank Not Found"
            self.ids.destinations_layout.clear_widgets()
            self.ids.destinations_layout.add_widget(Label(text=f"Error: Could not load data for Rank ID {rank_id}", color=COLOR_DANGER_PY, size_hint_y=None, height=dp(40)))
            self.ids.timestamp_label.text = ""

    def report_availability(self):
        # Placeholder: Logic to open a reporting dialog/screen
        if not self.rank_id:
             print("REPORT AVAILABILITY: No rank selected.")
             return # Maybe show a popup?
        print(f"REPORT AVAILABILITY button pressed for Rank ID: {self.rank_id}")
        # In a real app, show a popup or navigate to a new screen
        # E.g., show a Popup with destination choices and status buttons

    def go_back(self):
        # More robust back navigation: Check previous screen if possible
        # For simplicity, just go back to the list view.
        # Could potentially check self.manager.previous_screen but needs care
        if self.manager:
             self.manager.current = 'rank_list'
        else:
             print("Error: ScreenManager not found.")


class MyRoutesScreen(Screen):
     def on_enter(self, *args):
        self.update_routes_list()

     def update_routes_list(self):
        routes_layout = self.ids.routes_layout
        routes_layout.clear_widgets()
        # Height binding already in KV string

        if not MY_ROUTES_DATA:
             routes_layout.add_widget(Label(text="No saved routes yet. Tap '+' to add.", color=COLOR_ACCENT_PY, size_hint_y=None, height=dp(40)))
             return

        for route in MY_ROUTES_DATA:
             item = RouteListItem(
                 origin=route['origin'],
                 destination=route['destination'],
                 status=route['status']
                 )
             routes_layout.add_widget(item)

     def add_route(self):
         # Placeholder: Logic to navigate to a screen for adding routes
         print("ADD NEW ROUTE button pressed.")
         # Maybe navigate to RankListScreen to select origin/destination?
         # Or open a dedicated "Add Route" screen.


class SettingsScreen(Screen):
     def trigger_sos(self):
         # Placeholder: Logic to confirm and send SOS
         print("SOS BUTTON PRESSED! (Simulation - Implement confirmation & action)")
         # Example: Show a confirmation Popup

     def share_journey(self):
         # Placeholder: Logic to select contacts and start sharing
         print("SHARE MY JOURNEY button pressed (Simulation)")

     def manage_profile(self):
         print("MANAGE PROFILE button pressed (Simulation)")

     def manage_alerts(self):
         print("MANAGE ALERTS button pressed (Simulation)")

     def manage_emergency_contacts(self):
         print("MANAGE EMERGENCY CONTACTS button pressed (Simulation)")


# --- Screen Manager (Python Class) ---
class KhuthazaAppManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Use NoTransition for faster switching during testing/prototyping
        self.transition = NoTransition()

# --- Main App Class (Python) ---
class KhuthazaApp(App):
    def build(self):
        self.title = "Khuthaza (Prototype)"
        # Load the KV string definitions *before* creating widgets based on them
        Builder.load_string(KV_STRING)

        # Create the ScreenManager (it will find rules in the loaded KV string)
        sm = KhuthazaAppManager()

        # Add instances of the screen classes defined in Python
        # The names ('map', 'rank_list', etc.) must match the KV rules <ScreenName>:
        sm.add_widget(MapScreen(name='map'))
        sm.add_widget(RankListScreen(name='rank_list'))
        sm.add_widget(RankDetailScreen(name='rank_detail'))
        sm.add_widget(MyRoutesScreen(name='my_routes'))
        sm.add_widget(SettingsScreen(name='settings'))

        # Set the initial screen
        sm.current = 'rank_list' # Start on the list screen for this example

        return sm # Return the configured ScreenManager as the root widget

    # --- Navigation Helper Methods (Called from KV on_release) ---
    def go_to_map(self):
        if self.root and isinstance(self.root, ScreenManager):
            self.root.current = 'map'

    def go_to_rank_list(self):
         if self.root and isinstance(self.root, ScreenManager):
            self.root.current = 'rank_list'

    def go_to_my_routes(self):
         if self.root and isinstance(self.root, ScreenManager):
            self.root.current = 'my_routes'

    def go_to_settings(self):
         if self.root and isinstance(self.root, ScreenManager):
            self.root.current = 'settings'


# --- Run the App ---
if __name__ == '__main__':
    KhuthazaApp().run()