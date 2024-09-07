from customtkinter import *
import emodetection as ed
import musiclassify as mc
import spotiplaycreator as spc
import webbrowser
import time

def open_url(url):
    webbrowser.open(url)

def emodetect(textbox2):
    emotion = ed.turn_on_camera_and_return_emotion()
    textbox2.delete("1.0", "end")  # Clear previous text in the textbox2
    textbox2.insert("1.0", emotion)  # Insert the detected emotion into the textbox2
    ask_detect_again(textbox2, emotion)

def noartistname():
    popup = CTk()
    popup.title("Artist Name")
    popup.geometry("200x150")
    
    label1 = CTkLabel(master=popup, text="Please Enter a Artist Name")
    label1.place(relx=0.5, rely=0.1, anchor="n")
    
    def yes_action():
        popup.destroy()  
    
    yes_btn = CTkButton(popup, text="Okay", command=yes_action)
    yes_btn.place(relx=0.5, rely=0.4, anchor="n")
    
    popup.mainloop()


def showplaylist(textbox1, textbox2, textbox3):
    # Call the classify_songs function to get the list of songs
    artist_name = textbox1.get("1.0", "end").strip()
    if artist_name=="":
        noartistname()
        return
    emotion = textbox2.get("1.0", "end").strip()
    textbox3.delete("1.0", "end")
    textbox3.insert("1.0", "Please Wait Collecting Songs .Web Page will automatically open.....")
    textbox3.update()
    
    time.sleep(2)
    # Open the web page with the playlist
    show_playlist_web_page(artist_name, emotion)
    textbox3.delete("1.0", "end")
    textbox3.insert("1.0", "Songs Generated Successfully.....")

def ask_detect_again(textbox2, emotion):
    popup = CTk()
    popup.title("Detect Again")
    popup.geometry("300x150")
    
    def yes_action():
        popup.destroy()  
        emodetect(textbox2)  

    def no_action(textbox2, emotion):
        popup.destroy()
        if emotion != "happy":
            choicepopup(textbox2)

    label1 = CTkLabel(master=popup, text="Detected Emotion: " + emotion)
    label1.place(relx=0.5, rely=0.1, anchor="n")
    
    yes_btn = CTkButton(popup, text="Yes, detect again", command=yes_action)
    yes_btn.place(relx=0.5, rely=0.4, anchor="n")

    no_btn = CTkButton(popup, text="No, keep current emotion", command=lambda: no_action(textbox2, emotion))
    no_btn.place(relx=0.5, rely=0.8, anchor="n")
    
    popup.mainloop()

def choicepopup(textbox2):
    popup = CTk()
    popup.title("Mood")
    popup.geometry("300x150")
    
    def yes_action():
        textbox2.delete("1.0", "end")  # Clear previous text in the textbox2
        textbox2.insert("1.0", "happy")
        popup.destroy()  
          

    def no_action():
        popup.destroy()

    label1 = CTkLabel(master=popup, text="Which type of music you want")
    label1.place(relx=0.5, rely=0.1, anchor="n")
    
    yes_btn = CTkButton(popup, text="Uplifting", command=yes_action)
    yes_btn.place(relx=0.5, rely=0.4, anchor="n")

    no_btn = CTkButton(popup, text="Mood Supportive", command=no_action)
    no_btn.place(relx=0.5, rely=0.8, anchor="n")
    
    popup.mainloop()

def show_playlist_web_page(artist_name, emotion):
    
    # Call the classify_songs function to get the list of songs
    playlist = mc.classify_songs(artist_name, emotion)

    
    # Create the HTML content for the playlist
    html_content = "<html><head><title>Playlist</title>"
    html_content += "<style>"
    html_content += "body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }"
    html_content += "h1 { color: #333; text-align: center; margin-top: 20px; }"
    html_content += "p { margin-bottom: 10px; }"
    html_content += "a { color: #0274D9; text-decoration: none; }"
    html_content += "a:hover { text-decoration: underline; }"
    html_content += ".container { max-width: 800px; margin: 0 auto; padding: 20px; }"
    html_content += "</style>"
    html_content += "</head><body>"
    html_content += "<div class='container'>"
    html_content += "<h1>Playlist</h1>"
    
    for song in playlist:
        track_name = song[0]
        track_url = song[1]
        html_content += f"<p><a href='{track_url}' target='_blank'>{track_name}</a></p>"
    
    html_content += "</div>"
    html_content += "</body></html>"
    
    # Write the HTML content to a temporary file
    with open("playlist.html", "w") as f:
        f.write(html_content)
    
    # Open the web page in the default web browser
    webbrowser.open("playlist.html")

def spotifyplaylist(textbox2,textbox3):
    textbox3.delete("1.0", "end")
    textbox3.insert("1.0", "Please Wait Generating Spotify Playlist.....")
    textbox3.update()
    emotion = textbox2.get("1.0", "end").strip()
    print(emotion)
    emotion=emotion.replace('\n','')
    spc.create_playlist_and_add_songs(emotion)
    textbox3.delete("1.0", "end")
    textbox3.insert("1.0", "Spotify Playlist Created Successfully.....")

# Set the appearance mode and default color theme
set_appearance_mode("dark")
set_default_color_theme("dark-blue")
CTk.default_font = ("Helvetica", 60)

# Create the main application window
app = CTk()
app.title("Mood Music")
app.geometry("600x700")

label3 = CTkLabel(master=app, text="Artist Name")
label3.place(relx=0.1, rely=0.1, anchor="n")
textbox1 = CTkTextbox(master=app, width=300, height=4)
textbox1.configure(state='normal')
textbox1.place(relx=0.6, rely=0.1, anchor="n")

detect_btn = CTkButton(master=app, text="Detect Emotion", corner_radius=32,
                       fg_color="#0274D9", font=("Helvetica",16),border_color="#FFCC70",
                       border_width=2, command=lambda: emodetect(textbox2))
detect_btn.place(relx=0.6, rely=0.2, anchor="n")

label2 = CTkLabel(master=app, text="Mood")
label2.place(relx=0.1, rely=0.3, anchor="n")

textbox2 = CTkTextbox(app, width=300, height=4)
textbox2.configure(state='normal')
textbox2.place(relx=0.6, rely=0.3, anchor="n")

showplaylis_btn = CTkButton(master=app, text="Show Playlist", corner_radius=32,
                             fg_color="#0274D9",font=("Helvetica",16), border_color="#FFCC70",
                             border_width=2, command=lambda: showplaylist(textbox1, textbox2, textbox3))
showplaylis_btn.place(relx=0.15, rely=0.4, anchor="n")

label3 = CTkLabel(master=app, text="Status")
label3.place(relx=0.1, rely=0.5, anchor="n")

textbox3 = CTkTextbox(app, width=400, height=60)
textbox3.configure(state='normal')
textbox3.place(relx=0.6, rely=0.5, anchor="n")

gensptoiplay = CTkButton(master=app, text="Generate Playlist in Spotify", corner_radius=32,
                             fg_color="#0274D9",font=("Helvetica",16), border_color="#FFCC70",
                             border_width=2, command=lambda: spotifyplaylist( textbox2,textbox3))
gensptoiplay.place(relx=0.5, rely=0.4, anchor="n")

# Start the GUI event loop
app.mainloop()
