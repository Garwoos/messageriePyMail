import tkinter

# Création de la fenêtre principale
class interface(tkinter.Tk):
    def __init__(self, window):
        self.window = window
        self.window.title("Interface graphique")
        self.window.geometry("1080x720")
        self.window.resizable(False, False)
        
        # Création de font de la fenêtre
        self.canvas_output, self.inner_frame = self.new_canvas(self.window)
         
        for i in range(100):
            self.display_text(self.canvas_output, f"Hello World {i}", 10, 10+(i*20))
            
        
        
    def new_canvas(self, surface, width=1060, height=650, backgroundcolor="white", pady=5):
        """
        Création du canvas de la fenêtre
        """
        frame = tkinter.Frame(surface)
        frame.pack(fill="both")

        canvas = tkinter.Canvas(frame, width=width, height=height, bg=backgroundcolor)
        canvas.pack(side="left", fill="both", pady=pady, expand=True)

        scrollbar = tkinter.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Création d'une frame interne dans le canvas
        inner_frame = tkinter.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Mise à jour de la taille de la zone de défilement
        inner_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

        return canvas, inner_frame

    def display_text(self, surface, text, x, y, font="Arial 12", color="black"):
        """
        Affichage du texte sur le canvas
        """
        tkinter.Label(surface, text=text, font=font, bg="white", fg=color, anchor="nw").pack()
    
    def scroll_up(self):
        """
        Faire défiler le contenu du canvas vers le haut
        """
        self.canvas_output.yview_scroll(-1, "units")
        
    def scroll_down(self):
        """
        Faire défiler le contenu du canvas vers le bas
        """
        self.canvas_output.yview_scroll(1, "units")
    
    def on_mouse_scroll(self, event):
        # On Windows, `event.delta` is positive for scroll up, negative for scroll down.
        # On MacOS, `event.delta` is negative for scroll up, positive for scroll down.
        # On Linux, `event.num` is 4 for scroll up, 5 for scroll down.
        if event.delta > 0 or event.num == 4:
            self.scroll_up()
        else:
            self.scroll_down()
    
    
        
if __name__ == "__main__":
    window = tkinter.Tk()
    interface(window)
    window.mainloop()