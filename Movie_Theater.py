import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
import random

class MovieTheaterSeatBooking:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Theater Seat Booking System")
        
        # Start in full screen mode
        self.root.state('zoomed')  # Start maximized on Windows
        # For Linux/Mac, use: self.root.attributes('-zoomed', True)
        
        self.root.configure(bg="#0a0a1a")
        
        # Initialize seat grid (5x5)
        self.seat_grid = [[0 for _ in range(5)] for _ in range(5)]
        
        # Track booked seats
        self.booked_seats = []
        
        # Track selected seat
        self.selected_seat = None
        
        # Setup colors and fonts
        self.setup_styles()
        
        # Create GUI
        self.create_gui()
        
        # Initialize with some random booked seats for demo
        self.initialize_demo_bookings()
        
        # Bind window resize event
        self.root.bind('<Configure>', self.on_window_resize)
        
    def setup_styles(self):
        """Setup color schemes and fonts"""
        # Color scheme
        self.bg_color = "#0a0a1a"
        self.screen_color = "#1a1a2e"
        self.seat_empty = "#2ecc71"
        self.seat_booked = "#e74c3c"
        self.seat_selected = "#3498db"
        self.seat_hover = "#f39c12"
        self.text_color = "#ecf0f1"
        self.accent_color = "#9b59b6"
        
    def create_gui(self):
        """Create the main GUI layout"""
        # Main container using grid for better layout control
        self.main_container = tk.Frame(self.root, bg=self.bg_color)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configure grid weights - 70% for theater, 30% for controls
        self.main_container.grid_columnconfigure(0, weight=7)  # Theater area
        self.main_container.grid_columnconfigure(1, weight=3)  # Controls area
        self.main_container.grid_rowconfigure(0, weight=1)     # Single row
        
        # Left frame - Theater Area
        self.left_frame = tk.Frame(self.main_container, bg=self.bg_color)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        # Right frame - Controls Area
        self.right_frame = tk.Frame(self.main_container, bg=self.bg_color)
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        
        # Create all components
        self.create_header()
        self.create_theater_screen()
        self.create_seat_grid()
        self.create_seat_legend()
        self.create_controls_panel()
        self.create_booking_info()
        self.create_statistics_panel()
        
    def create_header(self):
        """Create header that spans both columns"""
        # Title at the top of left frame
        title_frame = tk.Frame(self.left_frame, bg=self.bg_color)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="🎬 MOVIE THEATER SEAT BOOKING SYSTEM",
            font=("Helvetica", 28, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            pady=10
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Select your seats by clicking or using the controls",
            font=("Helvetica", 14),
            bg=self.bg_color,
            fg="#95a5a6"
        )
        subtitle_label.pack()
        
    def create_theater_screen(self):
        """Create the theater screen visualization"""
        screen_frame = tk.Frame(self.left_frame, bg=self.bg_color)
        screen_frame.pack(fill=tk.X, pady=(0, 40))
        
        # Screen label
        self.screen_label = tk.Label(
            screen_frame,
            text="══════════════════════ S C R E E N ══════════════════════",
            font=("Helvetica", 18, "bold"),
            bg=self.screen_color,
            fg="#f1c40f",
            height=2,
            relief=tk.SUNKEN,
            bd=5
        )
        self.screen_label.pack(fill=tk.X, pady=10, padx=10)
        
    def create_seat_grid(self):
        """Create the 5x5 seat grid"""
        # Container for the grid
        grid_container = tk.Frame(self.left_frame, bg=self.bg_color)
        grid_container.pack(expand=True, fill=tk.BOTH, pady=(0, 30))
        
        # Create a frame for the actual grid with a border
        grid_frame = tk.Frame(grid_container, bg=self.bg_color, highlightbackground="#34495e", 
                              highlightthickness=2, highlightcolor="#34495e")
        grid_frame.pack(expand=True)
        
        # Configure grid for 5x5 seats
        for i in range(6):  # 5 seats + 1 for row labels
            grid_frame.grid_rowconfigure(i, weight=1)
            grid_frame.grid_columnconfigure(i, weight=1)
        
        # Create column headers (1-5)
        for col in range(5):
            col_label = tk.Label(
                grid_frame,
                text=f"SEAT {col+1}",
                font=("Helvetica", 14, "bold"),
                bg=self.bg_color,
                fg=self.text_color,
                padx=15,
                pady=10
            )
            col_label.grid(row=0, column=col+1, sticky="nsew")
        
        # Create row labels (A-E) and seat buttons
        self.seat_buttons = [[None for _ in range(5)] for _ in range(5)]
        
        for row in range(5):
            # Row label
            row_label = tk.Label(
                grid_frame,
                text=f"ROW {chr(65+row)}",
                font=("Helvetica", 14, "bold"),
                bg=self.bg_color,
                fg=self.text_color,
                padx=15,
                pady=10
            )
            row_label.grid(row=row+1, column=0, sticky="nsew")
            
            # Seat buttons for this row
            for col in range(5):
                seat_frame = tk.Frame(grid_frame, bg=self.bg_color)
                seat_frame.grid(row=row+1, column=col+1, padx=10, pady=10, sticky="nsew")
                
                btn = tk.Button(
                    seat_frame,
                    text=f"{chr(65+row)}{col+1}",
                    font=("Helvetica", 16, "bold"),
                    bg=self.seat_empty,
                    fg="white",
                    activebackground=self.seat_hover,
                    activeforeground="white",
                    relief=tk.RAISED,
                    bd=3,
                    width=6,
                    height=2,
                    command=lambda r=row, c=col: self.select_seat(r, c)
                )
                btn.pack(expand=True, fill=tk.BOTH)
                
                # Bind hover events
                btn.bind("<Enter>", lambda e, r=row, c=col: self.on_seat_hover(r, c, True))
                btn.bind("<Leave>", lambda e, r=row, c=col: self.on_seat_hover(r, c, False))
                
                self.seat_buttons[row][col] = btn
    
    def create_seat_legend(self):
        """Create seat status legend"""
        legend_frame = tk.Frame(self.left_frame, bg=self.bg_color)
        legend_frame.pack(fill=tk.X, pady=(0, 20))
        
        legend_title = tk.Label(
            legend_frame,
            text="SEAT STATUS LEGEND",
            font=("Helvetica", 16, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            pady=10
        )
        legend_title.pack()
        
        # Legend items in a horizontal layout
        legend_items_frame = tk.Frame(legend_frame, bg=self.bg_color)
        legend_items_frame.pack()
        
        legend_items = [
            ("Available", self.seat_empty),
            ("Booked", self.seat_booked),
            ("Selected", self.seat_selected),
            ("Hover", self.seat_hover)
        ]
        
        for text, color in legend_items:
            item_frame = tk.Frame(legend_items_frame, bg=self.bg_color)
            item_frame.pack(side=tk.LEFT, padx=20, pady=10)
            
            # Color box
            color_box = tk.Label(
                item_frame,
                bg=color,
                width=4,
                height=2,
                relief=tk.SUNKEN,
                bd=2
            )
            color_box.pack(side=tk.LEFT, padx=(0, 10))
            
            # Text label
            text_label = tk.Label(
                item_frame,
                text=text,
                font=("Helvetica", 12),
                bg=self.bg_color,
                fg=self.text_color
            )
            text_label.pack(side=tk.LEFT)
    
    def create_controls_panel(self):
        """Create the booking controls panel"""
        # Main controls container
        controls_container = tk.Frame(self.right_frame, bg=self.bg_color)
        controls_container.pack(fill=tk.BOTH, expand=True)
        
        # Controls Frame
        controls_frame = tk.LabelFrame(
            controls_container,
            text="🎯 BOOKING CONTROLS",
            font=("Helvetica", 18, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            padx=25,
            pady=25,
            relief=tk.RAISED,
            bd=3
        )
        controls_frame.pack(fill=tk.BOTH, expand=True)
        
        # Row selection
        row_frame = tk.Frame(controls_frame, bg=self.bg_color)
        row_frame.pack(fill=tk.X, pady=(0, 20))
        
        row_label = tk.Label(
            row_frame,
            text="SELECT ROW:",
            font=("Helvetica", 14, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            anchor="w"
        )
        row_label.pack(fill=tk.X, pady=(0, 10))
        
        self.row_var = tk.StringVar(value="A")
        row_buttons_frame = tk.Frame(row_frame, bg=self.bg_color)
        row_buttons_frame.pack(fill=tk.X)
        
        # Row selection buttons (A-E)
        for row_char in ["A", "B", "C", "D", "E"]:
            btn = tk.Radiobutton(
                row_buttons_frame,
                text=row_char,
                variable=self.row_var,
                value=row_char,
                font=("Helvetica", 16, "bold"),
                bg=self.bg_color,
                fg=self.text_color,
                selectcolor=self.accent_color,
                indicatoron=0,
                width=4,
                height=2,
                command=lambda rc=row_char: self.on_row_change(rc)
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # Seat number selection
        seat_frame = tk.Frame(controls_frame, bg=self.bg_color)
        seat_frame.pack(fill=tk.X, pady=(0, 20))
        
        seat_label = tk.Label(
            seat_frame,
            text="SELECT SEAT NUMBER:",
            font=("Helvetica", 14, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            anchor="w"
        )
        seat_label.pack(fill=tk.X, pady=(0, 10))
        
        self.seat_var = tk.IntVar(value=1)
        seat_buttons_frame = tk.Frame(seat_frame, bg=self.bg_color)
        seat_buttons_frame.pack(fill=tk.X)
        
        # Seat number buttons (1-5)
        for seat_num in [1, 2, 3, 4, 5]:
            btn = tk.Radiobutton(
                seat_buttons_frame,
                text=str(seat_num),
                variable=self.seat_var,
                value=seat_num,
                font=("Helvetica", 16, "bold"),
                bg=self.bg_color,
                fg=self.text_color,
                selectcolor=self.accent_color,
                indicatoron=0,
                width=4,
                height=2,
                command=lambda sn=seat_num: self.on_seat_change(sn)
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # Button container
        button_container = tk.Frame(controls_frame, bg=self.bg_color)
        button_container.pack(fill=tk.X, pady=(20, 0))
        
        # Book Selected Seat button
        self.book_button = tk.Button(
            button_container,
            text="🎫 BOOK SELECTED SEAT",
            command=self.book_seat_manual,
            font=("Helvetica", 16, "bold"),
            bg=self.accent_color,
            fg="white",
            activebackground="#8e44ad",
            activeforeground="white",
            relief=tk.RAISED,
            bd=4,
            height=2
        )
        self.book_button.pack(fill=tk.X, pady=(0, 15))
        
        # Book Random Seat button
        random_button = tk.Button(
            button_container,
            text="🎲 BOOK RANDOM AVAILABLE SEAT",
            command=self.book_random_seat,
            font=("Helvetica", 14, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            relief=tk.RAISED,
            bd=3,
            height=2
        )
        random_button.pack(fill=tk.X, pady=(0, 15))
        
        # Reset All Bookings button
        reset_button = tk.Button(
            button_container,
            text="🔄 RESET ALL BOOKINGS",
            command=self.reset_all_bookings,
            font=("Helvetica", 14, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            relief=tk.RAISED,
            bd=3,
            height=2
        )
        reset_button.pack(fill=tk.X)
    
    def create_booking_info(self):
        """Create booking information panel"""
        # Info container
        info_container = tk.Frame(self.right_frame, bg=self.bg_color)
        info_container.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Info Frame
        info_frame = tk.LabelFrame(
            info_container,
            text="📋 BOOKING INFORMATION",
            font=("Helvetica", 18, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            padx=25,
            pady=25,
            relief=tk.RAISED,
            bd=3
        )
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Current Selection Section
        selection_frame = tk.Frame(info_frame, bg=self.bg_color)
        selection_frame.pack(fill=tk.X, pady=(0, 25))
        
        selection_title = tk.Label(
            selection_frame,
            text="CURRENT SELECTION",
            font=("Helvetica", 16, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        selection_title.pack(anchor="w", pady=(0, 15))
        
        # Selected seat display
        selected_display_frame = tk.Frame(selection_frame, bg=self.bg_color, 
                                         highlightbackground=self.seat_selected,
                                         highlightthickness=2)
        selected_display_frame.pack(fill=tk.X, pady=10)
        
        selected_label = tk.Label(
            selected_display_frame,
            text="SELECTED SEAT:",
            font=("Helvetica", 14),
            bg=self.bg_color,
            fg="#95a5a6"
        )
        selected_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.selected_info = tk.Label(
            selected_display_frame,
            text="NONE",
            font=("Helvetica", 32, "bold"),
            bg=self.bg_color,
            fg=self.seat_selected
        )
        self.selected_info.pack(pady=(0, 15))
        
        # Status Section
        status_frame = tk.Frame(info_frame, bg=self.bg_color)
        status_frame.pack(fill=tk.X, pady=(0, 25))
        
        status_title = tk.Label(
            status_frame,
            text="BOOKING STATUS",
            font=("Helvetica", 16, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        status_title.pack(anchor="w", pady=(0, 15))
        
        self.booking_status = tk.Label(
            status_frame,
            text="Ready to book - Select a seat",
            font=("Helvetica", 14),
            bg=self.bg_color,
            fg=self.seat_empty,
            wraplength=300,
            justify=tk.LEFT
        )
        self.booking_status.pack(anchor="w")
        
        # Last Booking Section
        last_frame = tk.Frame(info_frame, bg=self.bg_color)
        last_frame.pack(fill=tk.X)
        
        last_title = tk.Label(
            last_frame,
            text="LAST BOOKING",
            font=("Helvetica", 16, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        last_title.pack(anchor="w", pady=(0, 15))
        
        self.last_booking_info = tk.Label(
            last_frame,
            text="No bookings yet",
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg=self.text_color,
            wraplength=300,
            justify=tk.LEFT
        )
        self.last_booking_info.pack(anchor="w")
    
    def create_statistics_panel(self):
        """Create statistics panel"""
        # Stats container
        stats_container = tk.Frame(self.right_frame, bg=self.bg_color)
        stats_container.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Stats Frame
        stats_frame = tk.LabelFrame(
            stats_container,
            text="📊 THEATER STATISTICS",
            font=("Helvetica", 18, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            padx=25,
            pady=25,
            relief=tk.RAISED,
            bd=3
        )
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        # Statistics grid
        stats_grid = tk.Frame(stats_frame, bg=self.bg_color)
        stats_grid.pack(fill=tk.BOTH, expand=True)
        
        # Total Seats
        total_frame = tk.Frame(stats_grid, bg=self.bg_color)
        total_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=10)
        
        total_label = tk.Label(
            total_frame,
            text="TOTAL SEATS",
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg="#95a5a6"
        )
        total_label.pack()
        
        self.total_seats_label = tk.Label(
            total_frame,
            text="25",
            font=("Helvetica", 24, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.total_seats_label.pack()
        
        # Available Seats
        available_frame = tk.Frame(stats_grid, bg=self.bg_color)
        available_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=10)
        
        available_label = tk.Label(
            available_frame,
            text="AVAILABLE",
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg="#95a5a6"
        )
        available_label.pack()
        
        self.available_seats_label = tk.Label(
            available_frame,
            text="25",
            font=("Helvetica", 24, "bold"),
            bg=self.bg_color,
            fg=self.seat_empty
        )
        self.available_seats_label.pack()
        
        # Booked Seats
        booked_frame = tk.Frame(stats_grid, bg=self.bg_color)
        booked_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=10)
        
        booked_label = tk.Label(
            booked_frame,
            text="BOOKED",
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg="#95a5a6"
        )
        booked_label.pack()
        
        self.booked_seats_label = tk.Label(
            booked_frame,
            text="0",
            font=("Helvetica", 24, "bold"),
            bg=self.bg_color,
            fg=self.seat_booked
        )
        self.booked_seats_label.pack()
        
        # Occupancy Rate
        occupancy_frame = tk.Frame(stats_grid, bg=self.bg_color)
        occupancy_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=10)
        
        occupancy_label = tk.Label(
            occupancy_frame,
            text="OCCUPANCY",
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg="#95a5a6"
        )
        occupancy_label.pack()
        
        self.occupancy_label = tk.Label(
            occupancy_frame,
            text="0%",
            font=("Helvetica", 24, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        self.occupancy_label.pack()
        
        # Progress bar for occupancy
        self.occupancy_bar = ttk.Progressbar(
            stats_frame,
            length=200,
            mode='determinate',
            maximum=100
        )
        self.occupancy_bar.pack(fill=tk.X, pady=(20, 10))
        
        # Configure grid weights
        stats_grid.grid_columnconfigure(0, weight=1)
        stats_grid.grid_columnconfigure(1, weight=1)
        stats_grid.grid_rowconfigure(0, weight=1)
        stats_grid.grid_rowconfigure(1, weight=1)
        
        # Update statistics
        self.update_statistics()
    
    def initialize_demo_bookings(self):
        """Initialize with some random booked seats for demonstration"""
        for _ in range(5):
            row = random.randint(0, 4)
            col = random.randint(0, 4)
            if self.seat_grid[row][col] == 0:
                self.seat_grid[row][col] = 1
                self.booked_seats.append((row, col))
        
        self.update_seat_display()
        self.update_statistics()
    
    def on_window_resize(self, event):
        """Handle window resize events"""
        if event.widget == self.root:
            # Update screen label to fit width
            screen_width = self.left_frame.winfo_width() - 40
            if screen_width > 100:
                # Adjust screen label width dynamically
                self.screen_label.config(width=screen_width // 8)
    
    def select_seat(self, row, col):
        """Handle seat selection via button click"""
        # Deselect previous selection
        if self.selected_seat:
            old_row, old_col = self.selected_seat
            if self.seat_grid[old_row][old_col] == 0:
                self.seat_buttons[old_row][old_col].config(bg=self.seat_empty)
        
        # Update selection
        self.selected_seat = (row, col)
        
        # Update seat display
        seat_name = f"{chr(65 + row)}{col + 1}"
        self.selected_info.config(text=seat_name)
        
        # Check if seat is available
        if self.seat_grid[row][col] == 0:
            self.seat_buttons[row][col].config(bg=self.seat_selected)
            self.booking_status.config(text="✅ Seat available for booking", fg=self.seat_empty)
        else:
            self.booking_status.config(text="❌ Seat already booked", fg=self.seat_booked)
        
        # Update input controls
        self.row_var.set(chr(65 + row))
        self.seat_var.set(col + 1)
    
    def on_seat_hover(self, row, col, enter):
        """Handle seat hover effects"""
        if self.selected_seat and self.selected_seat == (row, col):
            return  # Don't change color of selected seat
        
        if enter and self.seat_grid[row][col] == 0:
            self.seat_buttons[row][col].config(bg=self.seat_hover)
        elif not enter and self.seat_grid[row][col] == 0:
            self.seat_buttons[row][col].config(bg=self.seat_empty)
    
    def on_row_change(self, row_char):
        """Handle row selection change"""
        if self.selected_seat:
            row = ord(row_char) - 65
            col = self.seat_var.get() - 1
            self.select_seat(row, col)
    
    def on_seat_change(self, seat_num):
        """Handle seat number change"""
        if self.selected_seat:
            row = ord(self.row_var.get()) - 65
            col = seat_num - 1
            self.select_seat(row, col)
    
    def book_seat_manual(self):
        """Book seat using manual input controls"""
        try:
            # Get row and seat from input
            row_char = self.row_var.get()
            seat_num = self.seat_var.get()
            
            # Validate inputs
            if row_char not in ['A', 'B', 'C', 'D', 'E']:
                messagebox.showerror("Invalid Input", "Row must be between A and E")
                return
            
            if seat_num < 1 or seat_num > 5:
                messagebox.showerror("Invalid Input", "Seat number must be between 1 and 5")
                return
            
            # Convert to indices
            row = ord(row_char) - 65
            col = seat_num - 1
            
            # Book the seat
            self.book_seat(row, col)
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
    
    def book_seat(self, row, col):
        """Book a specific seat"""
        # Validate indices
        if row < 0 or row > 4 or col < 0 or col > 4:
            messagebox.showerror("Invalid Seat", "Row and seat must be between 0-4")
            return
        
        # Check if seat is available
        if self.seat_grid[row][col] == 0:
            # Update seat grid
            self.seat_grid[row][col] = 1
            self.booked_seats.append((row, col))
            
            # Update seat display
            self.update_seat_display()
            
            # Update statistics
            self.update_statistics()
            
            # Show confirmation
            seat_name = f"{chr(65 + row)}{col + 1}"
            self.last_booking_info.config(text=f"✅ Seat {seat_name} booked successfully")
            
            # Success message
            messagebox.showinfo(
                "🎉 Booking Confirmed!",
                f"✅ Seat {seat_name} has been successfully booked!\n\n"
                f"📍 Location: Row {chr(65 + row)}, Seat {col + 1}\n"
                f"📊 Total booked seats: {len(self.booked_seats)}\n"
                f"🎬 Enjoy your movie!"
            )
            
            # Update booking status
            self.booking_status.config(text=f"✅ Seat {seat_name} booked", fg=self.seat_booked)
            
            # Clear selection
            self.selected_seat = None
            self.selected_info.config(text="NONE")
            
        else:
            # Seat already booked
            seat_name = f"{chr(65 + row)}{col + 1}"
            messagebox.showwarning(
                "⚠️ Seat Unavailable",
                f"❌ Seat {seat_name} is already booked!\n\n"
                f"Please select another available seat."
            )
            
            # Update booking status
            self.booking_status.config(text=f"❌ Seat {seat_name} already taken", fg=self.seat_booked)
    
    def book_random_seat(self):
        """Book a random available seat"""
        available_seats = []
        
        # Find all available seats
        for row in range(5):
            for col in range(5):
                if self.seat_grid[row][col] == 0:
                    available_seats.append((row, col))
        
        if not available_seats:
            messagebox.showinfo("No Seats Available", "🎫 All seats are already booked!")
            return
        
        # Select random available seat
        row, col = random.choice(available_seats)
        
        # Select and book the seat
        self.select_seat(row, col)
        self.book_seat(row, col)
    
    def reset_all_bookings(self):
        """Reset all bookings"""
        if not self.booked_seats:
            messagebox.showinfo("No Bookings", "There are no bookings to reset.")
            return
        
        # Confirm reset
        response = messagebox.askyesno(
            "⚠️ Confirm Reset",
            f"Are you sure you want to reset all bookings?\n\n"
            f"This will clear {len(self.booked_seats)} booked seats."
        )
        
        if response:
            # Reset seat grid
            self.seat_grid = [[0 for _ in range(5)] for _ in range(5)]
            self.booked_seats = []
            self.selected_seat = None
            
            # Update UI
            self.update_seat_display()
            self.update_statistics()
            
            # Reset info labels
            self.selected_info.config(text="NONE")
            self.booking_status.config(text="✅ All bookings cleared - Ready to book", fg=self.seat_empty)
            self.last_booking_info.config(text="No bookings yet")
            
            messagebox.showinfo("✅ Reset Complete", "All bookings have been cleared successfully.")
    
    def update_seat_display(self):
        """Update the visual display of all seats"""
        for row in range(5):
            for col in range(5):
                if self.seat_grid[row][col] == 0:
                    # Empty seat
                    if self.selected_seat and self.selected_seat == (row, col):
                        self.seat_buttons[row][col].config(
                            bg=self.seat_selected,
                            state="normal"
                        )
                    else:
                        self.seat_buttons[row][col].config(
                            bg=self.seat_empty,
                            state="normal"
                        )
                else:
                    # Booked seat
                    self.seat_buttons[row][col].config(
                        bg=self.seat_booked,
                        state="disabled"
                    )
    
    def update_statistics(self):
        """Update statistics display"""
        total_seats = 25
        booked_seats = len(self.booked_seats)
        available_seats = total_seats - booked_seats
        occupancy_rate = (booked_seats / total_seats) * 100
        
        # Update labels
        self.available_seats_label.config(text=str(available_seats))
        self.booked_seats_label.config(text=str(booked_seats))
        self.occupancy_label.config(text=f"{occupancy_rate:.1f}%")
        
        # Update progress bar
        self.occupancy_bar['value'] = occupancy_rate
        
        # Update progress bar color based on occupancy
        if occupancy_rate < 30:
            self.occupancy_bar.config(style="green.Horizontal.TProgressbar")
        elif occupancy_rate < 70:
            self.occupancy_bar.config(style="yellow.Horizontal.TProgressbar")
        else:
            self.occupancy_bar.config(style="red.Horizontal.TProgressbar")

def main():
    """Main function to run the application"""
    root = tk.Tk()
    
    # Configure progress bar styles
    style = ttk.Style()
    style.theme_use('clam')
    
    # Create custom progress bar styles
    style.configure(
        "green.Horizontal.TProgressbar",
        troughcolor='#2c3e50',
        background='#2ecc71',
        lightcolor='#2ecc71',
        darkcolor='#27ae60'
    )
    
    style.configure(
        "yellow.Horizontal.TProgressbar",
        troughcolor='#2c3e50',
        background='#f1c40f',
        lightcolor='#f1c40f',
        darkcolor='#f39c12'
    )
    
    style.configure(
        "red.Horizontal.TProgressbar",
        troughcolor='#2c3e50',
        background='#e74c3c',
        lightcolor='#e74c3c',
        darkcolor='#c0392b'
    )
    
    # Create and run the application
    app = MovieTheaterSeatBooking(root)
    root.mainloop()

if __name__ == "__main__":
    main()