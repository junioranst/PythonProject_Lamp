import os
import sys
import customtkinter as ctk
from main import *
from CTkColorPicker import AskColor


# Configurações globais de tema e aparência
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


def get_resource_path(relative_path):
    """ Retorna o caminho correto para arquivos estáticos no .exe compilado """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


class ModernSmartHomeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Junioran Light Control")
        self.geometry("520x800")
        self.resizable(False, False)
        self.configure(fg_color="#0D0D0E")

        # Define o ícone da janela
        caminho_icone = get_resource_path("killzone.ico")
        try:
            self.iconbitmap(caminho_icone)
        except Exception:
            pass

        # Estado inicial das lâmpadas
        self.lamp1_state = {
            "power": False,
            "mode": "Desligado",
            "hex": "#FFFFFF",
            "temp": 0,
            "brightness": 100
        }
        self.lamp2_state = {
            "power": False,
            "mode": "Desligado",
            "hex": "#FFFFFF",
            "temp": 0,
            "brightness": 100
        }

        self.temperature_after_id = None
        self.brightness_after_id = None

        self.create_widgets()

    def create_widgets(self):
        # --- CABEÇALHO ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(25, 10))

        title = ctk.CTkLabel(
            header_frame,
            text="💡 Junioran's HUB",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#FFFFFF"
        )
        title.pack(side="left")

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Lamp Norte // Lamp Sul",
            font=ctk.CTkFont(size=12),
            text_color="#8A8A93"
        )
        subtitle.pack(side="right", pady=(8, 0))

        # --- SELEÇÃO DE ALVO ---
        target_card = ctk.CTkFrame(self, fg_color="#161618", corner_radius=18)
        target_card.pack(fill="x", padx=20, pady=10)

        target_title = ctk.CTkLabel(
            target_card,
            text="Controle das Lampadas",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#A1A1AA"
        )
        target_title.pack(pady=(12, 6))

        self.target_segmented = ctk.CTkSegmentedButton(
            target_card,
            values=["Ambas", "Lâmpada 1", "Lâmpada 2"],
            font=ctk.CTkFont(size=13, weight="bold"),
            selected_color="#D63031",
            selected_hover_color="#B71C1C",
            unselected_color="#242427",
            unselected_hover_color="#323236",
            text_color="#FFFFFF"
        )
        self.target_segmented.set("Ambas")
        self.target_segmented.pack(fill="x", padx=15, pady=(0, 15))

        # --- CARDS VISUAIS DE STATUS ---
        status_frame = ctk.CTkFrame(self, fg_color="transparent")
        status_frame.pack(fill="x", padx=20, pady=5)

        # Card Lâmpada 1
        self.l1_card = ctk.CTkFrame(status_frame, fg_color="#161618", corner_radius=18, border_width=2,
                                    border_color="#242427")
        self.l1_card.pack(side="left", expand=True, fill="both", padx=(0, 8))

        self.l1_icon = ctk.CTkLabel(self.l1_card, text="💡", font=ctk.CTkFont(size=36))
        self.l1_icon.pack(pady=(15, 2))

        self.l1_name = ctk.CTkLabel(self.l1_card, text="Lâmpada 1", font=ctk.CTkFont(size=14, weight="bold"),
                                    text_color="#FFFFFF")
        self.l1_name.pack()

        self.l1_status_lbl = ctk.CTkLabel(self.l1_card, text="Desligado", font=ctk.CTkFont(size=12),
                                          text_color="#71717A")
        self.l1_status_lbl.pack(pady=(2, 12))

        # Card Lâmpada 2
        self.l2_card = ctk.CTkFrame(status_frame, fg_color="#161618", corner_radius=18, border_width=2,
                                    border_color="#242427")
        self.l2_card.pack(side="right", expand=True, fill="both", padx=(8, 0))

        self.l2_icon = ctk.CTkLabel(self.l2_card, text="💡", font=ctk.CTkFont(size=36))
        self.l2_icon.pack(pady=(15, 2))

        self.l2_name = ctk.CTkLabel(self.l2_card, text="Lâmpada 2", font=ctk.CTkFont(size=14, weight="bold"),
                                    text_color="#FFFFFF")
        self.l2_name.pack()

        self.l2_status_lbl = ctk.CTkLabel(self.l2_card, text="Desligado", font=ctk.CTkFont(size=12),
                                          text_color="#71717A")
        self.l2_status_lbl.pack(pady=(2, 12))

        # --- PAINEL DE CONTROLES ---
        ctrl_card = ctk.CTkFrame(self, fg_color="#161618", corner_radius=18)
        ctrl_card.pack(fill="x", padx=20, pady=10)

        # Botões Master On / Off
        power_frame = ctk.CTkFrame(ctrl_card, fg_color="transparent")
        power_frame.pack(fill="x", padx=15, pady=15)

        btn_on = ctk.CTkButton(
            power_frame,
            text="⚡ Ligar",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2B5278",         # Azul suave/desbotado
            hover_color="#0984E3",      # Azul vivo ao passar o mouse
            corner_radius=12,
            height=40,
            command=lambda: self.set_power(True)
        )
        btn_on.pack(side="left", expand=True, fill="x", padx=(0, 6))

        btn_off = ctk.CTkButton(
            power_frame,
            text="🔌 Desligar",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#8B3A3A",         # Vermelho suave/desbotado
            hover_color="#D63031",      # Vermelho vivo ao passar o mouse
            corner_radius=12,
            height=40,
            command=lambda: self.set_power(False)
        )
        btn_off.pack(side="right", expand=True, fill="x", padx=(6, 0))

        # --- SLIDER TEMPERATURA DE COR ---
        temp_header = ctk.CTkFrame(ctrl_card, fg_color="transparent")
        temp_header.pack(fill="x", padx=15, pady=(5, 0))

        ctk.CTkLabel(temp_header, text="🌡️ Temperatura de Cor", font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#E4E4E7").pack(side="left")
        self.temp_val_lbl = ctk.CTkLabel(temp_header, text="0 (Branca)", font=ctk.CTkFont(size=12, weight="bold"),
                                         text_color="#FF4D4D")
        self.temp_val_lbl.pack(side="right")

        self.temp_slider = ctk.CTkSlider(
            ctrl_card,
            from_=0,
            to=100,
            number_of_steps=100,
            button_color="#FF3B30",
            button_hover_color="#D63031",
            progress_color="#FDCB6E",
            command=self.change_temperature
        )
        self.temp_slider.set(0)
        self.temp_slider.pack(fill="x", padx=15, pady=(5, 15))

        # --- SLIDER INTENSIDADE / BRILHO ---
        bright_header = ctk.CTkFrame(ctrl_card, fg_color="transparent")
        bright_header.pack(fill="x", padx=15, pady=(5, 0))

        ctk.CTkLabel(bright_header, text="☀️ Intensidade do Brilho", font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#E4E4E7").pack(side="left")
        self.bright_val_lbl = ctk.CTkLabel(bright_header, text="100%", font=ctk.CTkFont(size=12, weight="bold"),
                                           text_color="#FF4D4D")
        self.bright_val_lbl.pack(side="right")

        self.bright_slider = ctk.CTkSlider(
            ctrl_card,
            from_=0,
            to=100,
            number_of_steps=100,
            button_color="#FF3B30",
            button_hover_color="#D63031",
            progress_color="#E63946",
            command=self.change_brightness
        )
        self.bright_slider.set(100)
        self.bright_slider.pack(fill="x", padx=15, pady=(5, 15))

        # --- BOTÃO MODO RGB ---
        btn_rgb = ctk.CTkButton(
            ctrl_card,
            text="🎨 Escolher Cor Personalizada (Modo RGB)",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#D63031",
            hover_color="#B71C1C",
            corner_radius=12,
            height=42,
            command=self.open_color_picker
        )
        btn_rgb.pack(fill="x", padx=15, pady=(5, 15))

        # --- RODAPÉ ---
        footer = ctk.CTkLabel(
            self,
            text="Powered by Junioran",
            font=ctk.CTkFont(size=11),
            text_color="#71717A"
        )
        footer.pack(side="bottom", pady=(5, 15))

    def temp_to_hex(self, temp_val):
        ratio = temp_val / 100.0
        r = 255
        g = int(255 - (55 * ratio))
        b = int(255 - (205 * ratio))
        return f"#{r:02x}{g:02x}{b:02x}"

    def apply_brightness_to_color(self, hex_color, brightness_pct):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        factor = max(brightness_pct, 5) / 100.0
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        return f"#{r:02x}{g:02x}{b:02x}"

    def get_selected_target(self):
        return self.target_segmented.get()

    def change_temperature(self, value):
        val = int(value)

        self.temp_val_lbl.configure(
            text=f"{val} ({'Branca' if val < 30 else 'Neutra' if val < 70 else 'Amarela'})"
        )

        target = self.get_selected_target()
        hex_color = self.temp_to_hex(val)
        real_temp_val = 100 - val

        if target in ["Lâmpada 1", "Ambas"]:
            self.lamp1_state["temp"] = real_temp_val
            self.lamp1_state["hex"] = hex_color

        if target in ["Lâmpada 2", "Ambas"]:
            self.lamp2_state["temp"] = real_temp_val
            self.lamp2_state["hex"] = hex_color

        self.update_ui()

        if self.temperature_after_id is not None:
            self.after_cancel(self.temperature_after_id)

        self.temperature_after_id = self.after(
            600,
            self.send_temperature
        )

    def send_temperature(self):
        target = self.get_selected_target()

        if target in ["Lâmpada 1", "Ambas"] and self.lamp1_state["power"]:
            lampada_Norte.set_white_percentage(
                brightness=self.lamp1_state["brightness"],
                colourtemp=self.lamp1_state["temp"]
            )

        if target in ["Lâmpada 2", "Ambas"] and self.lamp2_state["power"]:
            lampada_Sul.set_white_percentage(
                brightness=self.lamp2_state["brightness"],
                colourtemp=self.lamp2_state["temp"]
            )

        self.temperature_after_id = None

    def change_brightness(self, value):
        val = int(value)

        self.bright_val_lbl.configure(text=f"{val}%")

        target = self.get_selected_target()

        if target in ["Lâmpada 1", "Ambas"]:
            self.lamp1_state["brightness"] = val

        if target in ["Lâmpada 2", "Ambas"]:
            self.lamp2_state["brightness"] = val

        self.update_ui()

        if self.brightness_after_id is not None:
            self.after_cancel(self.brightness_after_id)

        self.brightness_after_id = self.after(
            900,
            self.send_brightness
        )

    def send_brightness(self):
        target = self.get_selected_target()

        if target in ["Lâmpada 1", "Ambas"] and self.lamp1_state["power"]:
            lampada_Norte.set_white_percentage(
                brightness=self.lamp1_state["brightness"],
                colourtemp=100 - self.lamp1_state["temp"]
            )

        if target in ["Lâmpada 2", "Ambas"] and self.lamp2_state["power"]:
            lampada_Sul.set_white_percentage(
                brightness=self.lamp2_state["brightness"],
                colourtemp=100 - self.lamp2_state["temp"]
            )

        self.brightness_after_id = None

    def set_power(self, power_status):
        target = self.get_selected_target()

        if target in ["Lâmpada 1", "Ambas"]:
            self.lamp1_state["power"] = power_status

            if power_status:
                Ligar_Norte()
            else:
                Desligar_Norte()

        if target in ["Lâmpada 2", "Ambas"]:
            self.lamp2_state["power"] = power_status

            if power_status:
                Ligar_Sul()
            else:
                Desligar_Sul()

        self.update_ui()

    def open_color_picker(self):
        pick_color = AskColor()
        color = pick_color.get()

        if color:
            target = self.get_selected_target()

            if target in ["Lâmpada 1", "Ambas"]:
                self.lamp1_state.update({
                    "power": True,
                    "mode": "RGB",
                    "hex": color
                })

            if target in ["Lâmpada 2", "Ambas"]:
                self.lamp2_state.update({
                    "power": True,
                    "mode": "RGB",
                    "hex": color
                })

            self.update_ui()
            self.send_rgb(color, target)

    def send_rgb(self, color, target):
        color = color.lstrip("#")

        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)

        if target in ["Lâmpada 1", "Ambas"]:
            lampada_Norte.set_colour(r, g, b)

        if target in ["Lâmpada 2", "Ambas"]:
            lampada_Sul.set_colour(r, g, b)

    def update_ui(self):
        if self.lamp1_state["power"]:
            active_color = self.apply_brightness_to_color(self.lamp1_state["hex"], self.lamp1_state["brightness"])
            self.l1_card.configure(border_color=active_color, fg_color="#241B1B")
            self.l1_icon.configure(text_color=active_color)
            self.l1_status_lbl.configure(
                text=f"LIGADO • {self.lamp1_state['brightness']}%\n{self.lamp1_state['mode']}",
                text_color="#0984E3"
            )
        else:
            self.l1_card.configure(border_color="#242427", fg_color="#161618")
            self.l1_icon.configure(text_color="#52525B")
            self.l1_status_lbl.configure(text="DESLIGADO", text_color="#71717A")

        if self.lamp2_state["power"]:
            active_color = self.apply_brightness_to_color(self.lamp2_state["hex"], self.lamp2_state["brightness"])
            self.l2_card.configure(border_color=active_color, fg_color="#241B1B")
            self.l2_icon.configure(text_color=active_color)
            self.l2_status_lbl.configure(
                text=f"LIGADO • {self.lamp2_state['brightness']}%\n{self.lamp2_state['mode']}",
                text_color="#0984E3"
            )
        else:
            self.l2_card.configure(border_color="#242427", fg_color="#161618")
            self.l2_icon.configure(text_color="#52525B")
            self.l2_status_lbl.configure(text="DESLIGADO", text_color="#71717A")


if __name__ == "__main__":
    app = ModernSmartHomeApp()
    app.mainloop()