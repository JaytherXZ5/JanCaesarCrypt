import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import *
import utils
import re  # import the regular expression module
import os  # import the operating system module

class Encrypt:
    def __init__(self, master):
        self.main_window = master
        self.main_window.geometry("500x350+150+150")
        self.main_window.title("ENCRYPT")

        self.main_bg = tk.PhotoImage(file=f"./assets/encrypt_bg.png")
        self.encrypt_btn_img = tk.PhotoImage(file=f"./assets/encrypt_btn.png")
        self.browse_btn_img = tk.PhotoImage(file=f"./assets/browse_btn.png")
        self.back_btn_img = tk.PhotoImage(file=f"./assets/back_btn.png")
        self.textbox_img = tk.PhotoImage(file=f"./assets/textBox.png")

        self.saveBtnImg = tk.PhotoImage(file=f"./assets/saveBtn.png")
        self.shiftBoxImg = tk.PhotoImage(file=f"./assets/shiftText.png")
        self.plusBtnImg = tk.PhotoImage(file=f"./assets/plusBtn.png")
        self.minusBtnImg = tk.PhotoImage(file=f"./assets/minusBtn.png")
        self.cypher_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                            'J',
                            'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1',
                            '2', '3', '4', '5', '6', '7', '8', '9']
        self.shift_results = []
        # Main Canvas BG
        utils.getCanvas(self.main_window, "#ffffff", self.main_bg, 0, 0, 500, 350, 250.0, 175.0, "ridge")
        # textbox
        utils.getCanvas(self.main_window, "#ffffff", self.textbox_img, 78, 83, 270, 19, 213, 93.5, "ridge")
        self.text = utils.getText(self.main_window, 78, 83, 270, 19)
        # encrypt the info button

        utils.get_btn(self.main_window, self.caesar_encrypt, self.encrypt_btn_img, 352, 296, 69, 21, "flat")
        # browse button
        utils.get_btn(self.main_window, self.browse_file, self.browse_btn_img, 348, 83, 74, 21, "flat")
        # back button
        utils.get_btn(self.main_window, self.back_btn, self.back_btn_img, 26, 43, 44, 20, "flat")

        # save_button
        utils.get_btn(self.main_window, self.save_text, self.saveBtnImg, 175, 296, 55, 19, "flat")
        # shift plus button
        utils.get_btn(self.main_window, self.increment, self.plusBtnImg, 330, 296, 22, 20, "flat")
        # shift minus button
        utils.get_btn(self.main_window, self.decrement, self.minusBtnImg, 230, 294, 22, 19, "flat")
        # shiftBox
        utils.getCanvas(self.main_window, "#ffffff", self.shiftBoxImg, 283, 296, 50, 16, 308.0, 304.0, "ridge")
        self.shiftBox = tk.Entry(self.main_window)
        self.shiftBox.place(x=250, y=295, width=83, height=16)
        self.shiftBox.insert(tk.END, "1")

        self.text_frame2 = tk.Frame(self.main_window, width=344, height=190)
        self.text_frame2.place(x=78, y=116)

        self.text2 = tk.Text(self.text_frame2, width=41, height=11, bg="#d9d9d9")
        self.text2.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.text_frame2)
        scrollbar.pack(side="right", fill="y")

        self.text2.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text2.yview)

        # set placeholder text on text2 widget
        self.text2.insert(tk.END, "Browse a txt file or paste to Encrypt")

        # bind the Button-1 event to clear the placeholder text
        self.text2.bind("<Button-1>", self.clear_placeholder)

    def increment(self):
        selected_value = int(self.shiftBox.get())
        if selected_value < 35:
            self.shiftBox.delete(0, tk.END)
            self.shiftBox.insert(tk.END, str(selected_value + 1))
        else:
            messagebox.showinfo("Warning", "Shift from 1 to 35 only")

    def decrement(self):
        selected_value = int(self.shiftBox.get())
        if selected_value > 1:
            self.shiftBox.delete(0, tk.END)
            self.shiftBox.insert(tk.END, str(selected_value - 1))
        else:
            messagebox.showinfo("Warning", "Shift from 1 to 35 only")

    ##########################################
    def caesar_encrypt(self):
        ciphertext = ""
        for char in  self.text2.get(1.0,tk.END):
            if char.upper() in self.cypher_list:
                char_code = self.cypher_list.index(char.upper())
                char_code = (char_code + int(self.shiftBox.get())) % len(self.cypher_list)
                ciphertext += self.cypher_list[char_code]
            else:
                ciphertext +=char
        self.text2.delete(0.0, tk.END)
        self.text2.insert(tk.END, ciphertext)

    def save_text(self):
        # Get the text from the textbox
        text = self.text2.get("1.0", "end-1c")

        # Open a messagebox prompt to ask if you want to save the text
        response = messagebox.askquestion("Save Text", "Do you want to save the text?")

        if response == 'yes':
            # Open a file dialog to choose the save directory and file name
            file_path = filedialog.asksaveasfilename(defaultextension=".txt")

            if file_path:
                # Save the text to the chosen file
                with open(file_path, 'w') as file:
                    file.write(text)
                messagebox.showinfo("Save Successful", "File saved successfully.")
            else:
                messagebox.showwarning("Save Canceled", "Save canceled.")
        else:
            messagebox.showinfo("Save Canceled", "Save canceled.")

    def remove_non_modulo36_chars(self, text):
        """
        This function takes a string as input and removes any characters that do not belong to the modulo 36 system.
        """
        # use a regular expression to remove any non-modulo 36 characters, and return the resulting string
        return re.sub(r'[^a-z0-9]', '', text.lower())

    #######################################################################
    def clear_placeholder(self, event):
        if self.text2.get("1.0", "end-1c") == "Browse a txt file or paste to Encrypt":
            self.text2.delete("1.0", "end")
        elif self.text.get("1.0", "end-1c") == "Browse a text file to load contents":
            self.text.delete("1.0", "end")

    def browse_file(self):
        # show file dialog to select a text file
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            # insert the file path into the text widget
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, file_path)

            # open the selected file and read its contents
            with open(file_path, "r") as f:
                file_contents = f.read()

            # insert the file contents into the second text widget
            self.text2.delete(1.0, tk.END)
            self.text2.insert(tk.END, file_contents)  ###########################################################

    def exit(self):
        self.new_window.destroy()  # destroy the second window

    def back_btn(self):
        self.main_window.withdraw()
        self.new_window = tk.Toplevel(self.main_window)
        self.new_window.protocol("VW_DELETE_WINDOW", self.exit)  # set the callback for closing the second window
        self.app = App(self.new_window)

##############################################################################################
###################################################################################################

class App:
    def __init__(self, master):
        self.main_window = master
        self.main_window.title("CRYPTOOL")
        self.main_window.geometry("500x350+150+150")

        self.main_bg = tk.PhotoImage(file=f"./assets/bg_main.png")
        self.img0 = tk.PhotoImage(file=f"./assets/decrypt_btn_main.png")
        self.img1 = tk.PhotoImage(file=f"./assets/encrypt_btn_main.png")

        # Main Canvas BG
        utils.getCanvas(self.main_window, "#ffffff", self.main_bg, 0, 0, 500, 350, 250.0, 175.0, "ridge")
        # decrypt button main window
        utils.get_btn(self.main_window, self.open_decrypt, self.img0, 134, 161, 93, 32, "flat")
        # encrypt button main window
        utils.get_btn(self.main_window, self.open_encrypt, self.img1, 286, 161, 93, 32, "flat")

    def exit(self):
        self.new_window.destroy()  # destroy the second window

    def open_encrypt(self):
        self.main_window.withdraw()
        self.new_window = tk.Toplevel(self.main_window)
        self.new_window.protocol("VW_DELETE_WINDOW", self.exit)  # set the callback for closing the second window
        self.app = Encrypt(self.new_window)

    def open_decrypt(self):
        self.main_window.withdraw()
        self.new_window = tk.Toplevel(self.main_window)
        self.new_window.protocol("VW_DELETE_WINDOW", self.exit)  # set the callback for closing the second window
        self.app = Decrypt(self.new_window)

#####################################################################
#####################################################################
#####################################################################
class Decrypt:


    def __init__(self, master):
        self.main_window = master
        self.main_window.geometry("500x350+150+150")
        self.main_window.title("DECRYPT")

        self.main_bg = tk.PhotoImage(file=f"./assets/decrypt_bg.png")
        self.decrypt_btn_img = tk.PhotoImage(file=f"./assets/decrypt_btn.png")
        self.browse_btn_img = tk.PhotoImage(file=f"./assets/browse_btn.png")
        self.back_btn_img = tk.PhotoImage(file=f"./assets/back_btn.png")
        self.textbox_img = tk.PhotoImage(file=f"./assets/textBox.png")

        self.saveBtnImg = tk.PhotoImage(file=f"./assets/saveBtn.png")
        self.shiftBoxImg = tk.PhotoImage(file=f"./assets/shiftText.png")
        self.plusBtnImg = tk.PhotoImage(file = f"./assets/plusBtn.png")
        self.minusBtnImg = tk.PhotoImage(file=f"./assets/minusBtn.png")
        self.cypher_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                       'J',
                       'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0','1','2','3','4','5','6','7','8','9']
        self.shift_results = []
        # Main Canvas BG
        utils.getCanvas(self.main_window, "#ffffff", self.main_bg, 0, 0, 500, 350,250.0, 175.0, "ridge")
        #textbox
        utils.getCanvas(self.main_window,"#ffffff", self.textbox_img, 78, 83, 270, 19, 213, 93.5,"ridge")
        self.text = utils.getText(self.main_window, 78, 83, 270, 19)
        #decrypt the info button

        utils.get_btn(self.main_window, self.caesar_decrypt,self.decrypt_btn_img,   352, 296,69,21, "flat")
        #browse button
        utils.get_btn(self.main_window, self.browse_file,self.browse_btn_img, 348, 83, 74, 21, "flat")
        #back button
        utils.get_btn(self.main_window, self.back_btn,self.back_btn_img, 26, 43, 44, 20, "flat")

        #save_button
        utils.get_btn(self.main_window,self.save_text, self.saveBtnImg,175,296,55,19, "flat")
        #shift plus button
        utils.get_btn(self.main_window, self.increment, self.plusBtnImg,330, 296, 22, 20, "flat")
        #shift minus button
        utils.get_btn(self.main_window,self.decrement, self.minusBtnImg,230, 294, 22, 19, "flat")
        #shiftBox
        utils.getCanvas(self.main_window, "#ffffff", self.shiftBoxImg, 283, 296, 50,16, 308.0,304.0, "ridge")
        self.shiftBox = tk.Entry(self.main_window)
        self.shiftBox.place(x=250,y=295, width=83, height=16)
        self.shiftBox.insert(tk.END, "breakthrough")

        self.text_frame2 = tk.Frame(self.main_window, width=344, height=190)
        self.text_frame2.place(x=78, y=116)

        self.text2 = tk.Text(self.text_frame2, width=41, height=11, bg= "#d9d9d9")
        self.text2.pack(side="left", fill="both", expand=True)



        scrollbar = tk.Scrollbar(self.text_frame2)
        scrollbar.pack(side="right", fill="y")

        self.text2.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text2.yview)

        # set placeholder text on text2 widget
        self.text2.insert(tk.END, "Browse a txt file or paste an Encrypted Text/Code here")

        # bind the Button-1 event to clear the placeholder text
        self.text2.bind("<Button-1>", self.clear_placeholder)

    def increment(self):
        current_input = self.shiftBox.get()
        if current_input == "breakthrough":
            self.shiftBox.delete(0,tk.END)
            self.shiftBox.insert(tk.END,"0")
        selected_value = int(self.shiftBox.get())
        if selected_value < 35:
            self.shiftBox.delete(0, tk.END)
            self.shiftBox.insert(tk.END, str(selected_value + 1))
        else:
            messagebox.showinfo("Warning", "Shift from 1 to 35 only")

    def decrement(self):
        current_input = self.shiftBox.get()
        if current_input == "breakthrough":
            self.shiftBox.delete(0, tk.END)
            self.shiftBox.insert(tk.END, "0")
        selected_value = int(self.shiftBox.get())
        if selected_value > 1:
            self.shiftBox.delete(0, tk.END)
            self.shiftBox.insert(tk.END, str(selected_value - 1))
        elif selected_value <= 1:
            self.shiftBox.delete(0, tk.END)
            self.shiftBox.insert(tk.END, "breakthrough")
##########################################
    def caesar_decrypt(self):

        ciphertext = self.text2.get(1.0,tk.END)
        mod36_chars = self.cypher_list
        self.text2.delete(0.0, tk.END)
        ciphertext=str(ciphertext)
        for shift in range(len(mod36_chars)):
            plaintext = ''
            for char in ciphertext:
                if char.upper() in mod36_chars:
                    # Determine the new character by shifting it by the shift value
                    char_code = mod36_chars.index(char.upper())
                    char_code = (char_code - shift) % len(mod36_chars)
                    plaintext += mod36_chars[char_code]

                else:
                    plaintext += char
            self.shift_results.append("Shift " + str(shift) + ": " + plaintext)
            shift_input = self.shiftBox.get()
        if shift_input == "breakthrough":
            for i in self.shift_results:
                print(i)
            self.text2.delete(0.0,tk.END)
            self.text2.insert(tk.END, self.shift_results)
        elif 1 <= int(shift_input) <= 35:
            shift = self.shift_results[int(shift_input)]
            self.text2.insert(tk.END, shift)
        else:
            messagebox.showinfo("Warning", "Invalid input. Enter a value between 1 and 10.")
        #for i in self.shift_results:
            #print(i)
        #self.text2.insert(tk.END, self.shift_results)#############################################################################################

    def save_text(self):
        # Get the text from the textbox
        text = self.text2.get("1.0", "end-1c")

        # Open a messagebox prompt to ask if you want to save the text
        response = messagebox.askquestion("Save Text", "Do you want to save the text?")

        if response == 'yes':
            # Open a file dialog to choose the save directory and file name
            file_path = filedialog.asksaveasfilename(defaultextension=".txt")

            if file_path:
                # Save the text to the chosen file
                with open(file_path, 'w') as file:
                    file.write(text)
                messagebox.showinfo("Save Successful", "File saved successfully.")
            else:
                messagebox.showwarning("Save Canceled", "Save canceled.")
        else:
            messagebox.showinfo("Save Canceled", "Save canceled.")
    def remove_non_modulo36_chars(self,text):
        """
        This function takes a string as input and removes any characters that do not belong to the modulo 36 system.
        """
        # use a regular expression to remove any non-modulo 36 characters, and return the resulting string
        return re.sub(r'[^a-z0-9]', '', text.lower())
#######################################################################
    def clear_placeholder(self,event):
        if self.text2.get("1.0", "end-1c") == "Browse a txt file or paste an Encrypted Text/Code here":
            self.text2.delete("1.0", "end")
        elif self.text.get("1.0", "end-1c") == "Browse a text file to load contents":
            self.text.delete("1.0", "end")

    def browse_file(self):
        # show file dialog to select a text file
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            # insert the file path into the text widget
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, file_path)

            # open the selected file and read its contents
            with open(file_path, "r") as f:
                file_contents = f.read()

            # insert the file contents into the second text widget
            self.text2.delete(1.0, tk.END)
            self.text2.insert(tk.END, file_contents)###########################################################

    def exit(self):
        self.new_window.destroy()  # destroy the second window

    def back_btn(self):
        self.main_window.withdraw()
        self.new_window = tk.Toplevel(self.main_window)
        self.new_window.protocol("VW_DELETE_WINDOW", self.exit)  # set the callback for closing the second window
        self.app = App(self.new_window)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()