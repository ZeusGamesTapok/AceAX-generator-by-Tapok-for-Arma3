import tkinter as tk
from tkinter import ttk, messagebox
import itertools

class UniformConfigGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Arma 3 Uniform Config Generator")
        self.master.geometry("1000x700")

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.cfg_patches_frame = ttk.Frame(self.notebook)
        self.uniform_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.cfg_patches_frame, text="CfgPatches")
        self.notebook.add(self.uniform_frame, text="Uniform")

        self.create_cfg_patches_widgets()
        self.create_uniform_widgets()

        self.generate_button = ttk.Button(self.master, text="Make Cfg", command=self.generate_config)
        self.generate_button.pack(pady=10)

    def create_cfg_patches_widgets(self):
        self.cfg_patches_canvas = tk.Canvas(self.cfg_patches_frame)
        self.cfg_patches_scrollbar = ttk.Scrollbar(self.cfg_patches_frame, orient="vertical", command=self.cfg_patches_canvas.yview)
        self.cfg_patches_scrollable_frame = ttk.Frame(self.cfg_patches_canvas)

        self.cfg_patches_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.cfg_patches_canvas.configure(
                scrollregion=self.cfg_patches_canvas.bbox("all")
            )
        )

        self.cfg_patches_canvas.create_window((0, 0), window=self.cfg_patches_scrollable_frame, anchor="nw")
        self.cfg_patches_canvas.configure(yscrollcommand=self.cfg_patches_scrollbar.set)

        self.cfg_patches_canvas.pack(side="left", fill="both", expand=True)
        self.cfg_patches_scrollbar.pack(side="right", fill="y")

        ttk.Label(self.cfg_patches_scrollable_frame, text="CfgPatches Class:").pack(anchor='w', padx=10, pady=5)
        self.cfg_patches_class = ttk.Entry(self.cfg_patches_scrollable_frame)
        self.cfg_patches_class.pack(fill=tk.X, padx=10, pady=5)
        self.cfg_patches_class.insert(0, "Cool_Mod")

        ttk.Label(self.cfg_patches_scrollable_frame, text="Required Addons:").pack(anchor='w', padx=10, pady=5)
        self.required_addons_frame = ttk.Frame(self.cfg_patches_scrollable_frame)
        self.required_addons_frame.pack(fill=tk.X, padx=10, pady=5)
        self.required_addons = []
        self.add_required_addon()

        ttk.Button(self.required_addons_frame, text="+", command=self.add_required_addon).pack(side=tk.LEFT)
        ttk.Button(self.required_addons_frame, text="-", command=self.remove_required_addon).pack(side=tk.LEFT)

        ttk.Label(self.cfg_patches_scrollable_frame, text="Author:").pack(anchor='w', padx=10, pady=5)
        self.author = ttk.Entry(self.cfg_patches_scrollable_frame)
        self.author.pack(fill=tk.X, padx=10, pady=5)
        self.author.insert(0, "Your Name")

    def create_uniform_widgets(self):
        self.uniform_canvas = tk.Canvas(self.uniform_frame)
        self.uniform_scrollbar = ttk.Scrollbar(self.uniform_frame, orient="vertical", command=self.uniform_canvas.yview)
        self.uniform_scrollable_frame = ttk.Frame(self.uniform_canvas)

        self.uniform_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.uniform_canvas.configure(
                scrollregion=self.uniform_canvas.bbox("all")
            )
        )

        self.uniform_canvas.create_window((0, 0), window=self.uniform_scrollable_frame, anchor="nw")
        self.uniform_canvas.configure(yscrollcommand=self.uniform_scrollbar.set)

        self.uniform_canvas.pack(side="left", fill="both", expand=True)
        self.uniform_scrollbar.pack(side="right", fill="y")

        self.create_cfg_weapon_widgets()
        self.create_cfg_vehicles_widgets()
        self.create_aceax_widgets()

    def create_cfg_weapon_widgets(self):
        ttk.Label(self.uniform_scrollable_frame, text="CfgWeapons").pack(anchor='w', padx=10, pady=5)
       
        ttk.Label(self.uniform_scrollable_frame, text="Picture:").pack(anchor='w', padx=10, pady=5)
        self.picture = ttk.Entry(self.uniform_scrollable_frame)
        self.picture.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self.uniform_scrollable_frame, text="Drop Model:").pack(anchor='w', padx=10, pady=5)
        self.drop_model = ttk.Entry(self.uniform_scrollable_frame)
        self.drop_model.pack(fill=tk.X, padx=10, pady=5)
        self.drop_model.insert(0, r"\A3\Characters_F\Common\Suitpacks\suitpack_original_F.p3d")

    def create_cfg_vehicles_widgets(self):
        ttk.Label(self.uniform_scrollable_frame, text="CfgVehicles").pack(anchor='w', padx=10, pady=5)

        ttk.Label(self.uniform_scrollable_frame, text="CfgVehicles Uniform_base class:").pack(anchor='w', padx=10, pady=5)
        self.cfg_vehicles_uniform_base_class = ttk.Entry(self.uniform_scrollable_frame)
        self.cfg_vehicles_uniform_base_class.pack(fill=tk.X, padx=10, pady=5)
        self.cfg_vehicles_uniform_base_class.insert(0, "Uniform_Base")

        ttk.Label(self.uniform_scrollable_frame, text="Uniform Mother class:").pack(anchor='w', padx=10, pady=5)
        self.uniform_mother_class = ttk.Entry(self.uniform_scrollable_frame)
        self.uniform_mother_class.pack(fill=tk.X, padx=10, pady=5)
        self.uniform_mother_class.insert(0, "uniformotherclass")

        ttk.Label(self.uniform_scrollable_frame, text="Mother Model Path:").pack(anchor='w', padx=10, pady=5)
        self.mother_model_path = ttk.Entry(self.uniform_scrollable_frame)
        self.mother_model_path.pack(fill=tk.X, padx=10, pady=5)
        self.mother_model_path.insert(0, "path.p3d")

        self.hidden_selections_frame = ttk.Frame(self.uniform_scrollable_frame)
        self.hidden_selections_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(self.hidden_selections_frame, text="HiddenSelectionsMother:").pack(side=tk.LEFT)
        self.hidden_selections = []
        self.add_hidden_selection()

        ttk.Button(self.hidden_selections_frame, text="+", command=self.add_hidden_selection).pack(side=tk.LEFT)
        ttk.Button(self.hidden_selections_frame, text="-", command=self.remove_hidden_selection).pack(side=tk.LEFT)

        self.hidden_textures_frame = ttk.Frame(self.uniform_scrollable_frame)
        self.hidden_textures_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(self.hidden_textures_frame, text="HiddenTextureMother:").pack(side=tk.LEFT)
        self.hidden_textures = []
        self.add_hidden_texture()

        ttk.Button(self.hidden_textures_frame, text="+", command=self.add_hidden_texture).pack(side=tk.LEFT)
        ttk.Button(self.hidden_textures_frame, text="-", command=self.remove_hidden_texture).pack(side=tk.LEFT)

    def create_aceax_widgets(self):
        ttk.Label(self.uniform_scrollable_frame, text="AceAx").pack(anchor='w', padx=10, pady=5)

        ttk.Label(self.uniform_scrollable_frame, text="AceAx Model:").pack(anchor='w', padx=10, pady=5)
        self.aceax_model = ttk.Entry(self.uniform_scrollable_frame)
        self.aceax_model.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self.uniform_scrollable_frame, text="AceAx Description:").pack(anchor='w', padx=10, pady=5)
        self.aceax_description = ttk.Entry(self.uniform_scrollable_frame)
        self.aceax_description.pack(fill=tk.X, padx=10, pady=5)
        self.aceax_description.insert(0, "putsomething")

        self.aceax_options_frame = ttk.Frame(self.uniform_scrollable_frame)
        self.aceax_options_frame.pack(fill=tk.X, padx=10, pady=5)
        self.aceax_options = []
        self.add_aceax_option()

        ttk.Button(self.aceax_options_frame, text="Add AceAx Option", command=self.add_aceax_option).pack()

    def add_required_addon(self):
        addon = ttk.Entry(self.required_addons_frame)
        addon.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
        self.required_addons.append(addon)

    def remove_required_addon(self):
        if self.required_addons:
            addon = self.required_addons.pop()
            addon.destroy()

    def add_hidden_selection(self):
        selection = ttk.Entry(self.hidden_selections_frame)
        selection.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
        self.hidden_selections.append(selection)

    def remove_hidden_selection(self):
        if self.hidden_selections:
            selection = self.hidden_selections.pop()
            selection.destroy()

    def add_hidden_texture(self):
        texture = ttk.Entry(self.hidden_textures_frame)
        texture.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
        self.hidden_textures.append(texture)

    def remove_hidden_texture(self):
        if self.hidden_textures:
            texture = self.hidden_textures.pop()
            texture.destroy()

    def add_aceax_option(self):
        option_frame = ttk.Frame(self.aceax_options_frame)
        option_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(option_frame, text="AceAx Option:").pack(side=tk.LEFT)
        option = ttk.Entry(option_frame)
        option.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(option_frame, text="Ace Ax hiddenSelection number:").pack(side=tk.LEFT)
        hidden_selection_number = ttk.Spinbox(option_frame, from_=1, to=100, width=5)
        hidden_selection_number.pack(side=tk.LEFT)

        values_frame = ttk.Frame(option_frame)
        values_frame.pack(fill=tk.X)

        values = []
        icons = []
        textures = []
        action_labels = []
        change_ingame_vars = []

        def add_value():
            value_frame = ttk.Frame(values_frame)
            value_frame.pack(fill=tk.X)

            value = ttk.Entry(value_frame, width=20)
            value.pack(side=tk.LEFT)
            values.append(value)

            icon = ttk.Entry(value_frame, width=20)
            icon.pack(side=tk.LEFT)
            icons.append(icon)

            texture = ttk.Entry(value_frame, width=20)
            texture.pack(side=tk.LEFT)
            textures.append(texture)

            change_ingame_var = tk.BooleanVar()
            change_ingame_check = ttk.Checkbutton(value_frame, text="changeingame", variable=change_ingame_var)
            change_ingame_check.pack(side=tk.LEFT)
            change_ingame_vars.append(change_ingame_var)

            action_label = ttk.Entry(value_frame, width=20)
            action_label.pack(side=tk.LEFT)
            action_labels.append(action_label)

            ttk.Button(value_frame, text="-", command=lambda: remove_value(value_frame)).pack(side=tk.LEFT)

        def remove_value(value_frame):
            for i, frame in enumerate(values_frame.winfo_children()):
                if frame == value_frame:
                    if i < len(values):
                        values.pop(i)
                        icons.pop(i)
                        textures.pop(i)
                        change_ingame_vars.pop(i)
                        action_labels.pop(i)
                    value_frame.destroy()
                    break        
        ttk.Button(values_frame, text="+", command=add_value).pack()

        add_value()  # Add first value by default

        self.aceax_options.append({
            'option': option,
            'hidden_selection_number': hidden_selection_number,
            'values': values,
            'icons': icons,
            'textures': textures,
            'change_ingame_vars': change_ingame_vars,
            'action_labels': action_labels
        })

    def generate_config(self):
        config = self.generate_cfg_patches()
        config += self.generate_cfg_weapons()
        config += self.generate_cfg_vehicles()
        config += self.generate_xtd_gear_models()

        config_window = tk.Toplevel(self.master)
        config_window.title("Generated Config")
        config_window.geometry("800x600")

        config_text = tk.Text(config_window, wrap=tk.NONE)
        config_text.pack(expand=True, fill='both')
        config_text.insert(tk.END, config)

        copy_button = ttk.Button(config_window, text="Copy", command=lambda: self.copy_to_clipboard(config))
        copy_button.pack(pady=10)

        self.show_debug_window()
    def generate_cfg_patches(self):
        cfg_patches = "class CfgPatches\n{\n"
        cfg_patches += f"    class {self.cfg_patches_class.get()}\n    {{\n"
        cfg_patches += "        requiredAddons[] =\n        {\n"
        for addon in self.required_addons:
            cfg_patches += f'            "{addon.get()}",\n'
        cfg_patches = cfg_patches.rstrip(',\n') + "\n"
        cfg_patches += "        };\n"
        cfg_patches += "        requiredVersion=1.60;\n"
        cfg_patches += f'        author="{self.author.get()}";\n'
        cfg_patches += "    };\n};\n\n"
        return cfg_patches

    def generate_cfg_weapons(self):
        cfg_weapons = "class CfgWeapons\n{\n"
        cfg_weapons += "    class ItemCore;\n"
        cfg_weapons += "    class UniformItem;\n"
        cfg_weapons += f"    class {self.cfg_vehicles_uniform_base_class.get()};\n"
        cfg_weapons += f"    class {self.uniform_mother_class.get()}: {self.cfg_vehicles_uniform_base_class.get()}\n    {{\n"
        cfg_weapons += "        scope=1;\n"
        cfg_weapons += f'        picture="{self.picture.get()}";\n'
        cfg_weapons += "        scopeArsenal=1;\n"
        cfg_weapons += f'        author="{self.author.get()}";\n'
        cfg_weapons += '        displayName="This_IS_Hidden";\n'
        cfg_weapons += f'        model="{self.drop_model.get()}";\n'
        cfg_weapons += "        class ItemInfo: UniformItem\n        {\n"
        cfg_weapons += f'            uniformModel="{self.mother_model_path.get()}";\n'
        cfg_weapons += f'            uniformClass="{self.uniform_mother_class.get()}";\n'
        cfg_weapons += "            containerClass=\"Supply20\";\n"
        cfg_weapons += "            mass=33.069;\n"
        cfg_weapons += "            allowedSlots[]={701,801,901};\n"
        cfg_weapons += "            armor=0;\n"
        cfg_weapons += "        };\n"
        cfg_weapons += "    };\n"

        for variant in self.generate_uniform_variants():
            cfg_weapons += self.generate_uniform_variant(variant)

        cfg_weapons += "};\n\n"
        return cfg_weapons

    def generate_uniform_variants(self):
        options = []
        for option in self.aceax_options:
            values = [value.get() for value in option['values'] if value.get()]
            if not values:
                print(f"Warning: No valid values for option {option['option'].get()}. Skipping this option.")
                continue
            options.append(values)
        return list(itertools.product(*options))

    def generate_uniform_variant(self, variant):
        variant_name = '_'.join(variant)
        uniform = f"    class {self.uniform_mother_class.get()}_{variant_name}: {self.uniform_mother_class.get()}\n    {{\n"
        uniform += f'        displayName="Uniform {variant_name}";\n'
        uniform += "        scope=2;\n"
        uniform += "        scopeArsenal=2;\n"
        uniform += "        class ItemInfo: ItemInfo\n        {\n"
        uniform += f'            uniformClass="{self.uniform_mother_class.get()}_{variant_name}";\n'
        uniform += "        };\n"
        uniform += "    };\n"
        return uniform

    def generate_cfg_vehicles(self):
        cfg_vehicles = "class CfgVehicles\n{\n"
        cfg_vehicles += "    class B_Soldier_F;\n"
        cfg_vehicles += "    class B_diver_F;\n"
        cfg_vehicles += f"    class {self.uniform_mother_class.get()}: B_Soldier_F\n    {{\n"
        cfg_vehicles += "        scope=2;\n"
        cfg_vehicles += f'        picture="{self.picture.get()}";\n'
        cfg_vehicles += "        camouflage=0;\n"
        cfg_vehicles += '        displayName="This_IS_Hidden";\n'
        cfg_vehicles += "        scopeArsenal=1;\n"
        cfg_vehicles += "        faction=\"\";\n"
        cfg_vehicles += f'        author="{self.author.get()}";\n'
        cfg_vehicles += f'        model="{self.mother_model_path.get()}";\n'
        cfg_vehicles += f'        uniformClass="{self.uniform_mother_class.get()}";\n'
        cfg_vehicles += "        identityTypes[]=\n        {\n"
        cfg_vehicles += '            "G_NATO_diver"\n'
        cfg_vehicles += "        };\n"
        cfg_vehicles += "        hiddenSelections[]=\n        {\n"
        for selection in self.hidden_selections:
            cfg_vehicles += f'            "{selection.get()}",\n'
        cfg_vehicles = cfg_vehicles.rstrip(',\n') + "\n"
        cfg_vehicles += "        };\n"
        cfg_vehicles += "        hiddenSelectionsTextures[]=\n        {\n"
        for texture in self.hidden_textures:
            cfg_vehicles += f'            "{texture.get()}",\n'
        cfg_vehicles = cfg_vehicles.rstrip(',\n') + "\n"
        cfg_vehicles += "        };\n"
        cfg_vehicles += "    };\n"
       
        for variant in self.generate_uniform_variants():
            cfg_vehicles += self.generate_vehicle_variant(variant)
       
        cfg_vehicles += "};\n\n"
        return cfg_vehicles

    def generate_vehicle_variant(self, variant):
        variant_name = '_'.join(variant)
        vehicle = f"    class {self.uniform_mother_class.get()}_{variant_name}: {self.uniform_mother_class.get()}\n    {{\n"
        vehicle += "        scope=2;\n"
        vehicle += f'        uniformClass="{self.uniform_mother_class.get()}_{variant_name}";\n'
        vehicle += "        hiddenSelectionsTextures[]=\n        {\n"
       
        for i, option in enumerate(self.aceax_options):
            try:
                value_index = option['values'].index(next(v for v in option['values'] if v.get() == variant[i]))
                texture = option["textures"][value_index].get()
            except (ValueError, StopIteration):
                print(f"Warning: Value '{variant[i]}' not found in option {option['option'].get()}. Using default texture.")
                texture = option["textures"][0].get() if option["textures"] else ""
           
            vehicle += f'            "{texture}",\n'
       
        vehicle = vehicle.rstrip(',\n') + "\n"
        vehicle += "        };\n"
        vehicle += "    };\n"
        return vehicle

    def generate_xtd_gear_models(self):
        xtd_gear_models = "class XtdGearModels\n{\n"
        xtd_gear_models += "    class CfgWeapons\n    {\n"
        xtd_gear_models += f"        class {self.aceax_model.get()}\n        {{\n"
        xtd_gear_models += "            label = \"Uniform\";\n"
        xtd_gear_models += f'            author = "{self.author.get()}";\n'
        xtd_gear_models += f'            description = "{self.aceax_description.get()}";\n'
   
        options = [f'"{option["option"].get()}"' for option in self.aceax_options]
        xtd_gear_models += f'            options[]={{\n                {", ".join(options)}\n            }};\n'
   
        for option in self.aceax_options:
            xtd_gear_models += f'            class {option["option"].get()}\n            {{\n'
            xtd_gear_models += f'                label = "{option["option"].get()}";\n'
       
            values = [f'"{value.get()}"' for value in option['values'] if value.get()]
            xtd_gear_models += f'                values[] = {{{", ".join(values)}}};\n'
       
            for i, value in enumerate(option['values']):
                if value.get():
                    xtd_gear_models += f'                class {value.get()}\n                {{\n'
                    xtd_gear_models += f'                    label = "{value.get()}";\n'
                    xtd_gear_models += f'                    image = "{option["icons"][i].get()}";\n'
                    xtd_gear_models += "                };\n"
            xtd_gear_models += "            };\n"
   
        xtd_gear_models += "        };\n"
        xtd_gear_models += "    };\n"
        xtd_gear_models += "};\n\n"

        xtd_gear_models += "class XtdGearInfos\n{\n"
        xtd_gear_models += "    class CfgWeapons\n    {\n"
   
        for variant in self.generate_uniform_variants():
            xtd_gear_models += self.generate_xtd_gear_info(variant)
   
        xtd_gear_models += "    };\n"
        xtd_gear_models += "};\n"

        return xtd_gear_models

    def generate_xtd_gear_info(self, variant):
        variant_name = '_'.join(variant)
        info = f"        class {self.uniform_mother_class.get()}_{variant_name}\n        {{\n"
        info += f'            model = "{self.aceax_model.get()}";\n'
   
        for i, option in enumerate(self.aceax_options):
            info += f'            {option["option"].get()} = "{variant[i]}";\n'
   
        info += "        };\n"
        return info

    def copy_to_clipboard(self, text):
        self.master.clipboard_clear()
        self.master.clipboard_append(text)
        messagebox.showinfo("Copied", "Config has been copied to clipboard!")

    def show_debug_window(self):
        debug_window = tk.Toplevel(self.master)
        debug_window.title("Debug Information")
        debug_window.geometry("400x400")

        debug_text = tk.Text(debug_window, wrap=tk.WORD)
        debug_text.pack(expand=True, fill='both')

        debug_info = f"Author: {self.author.get()}\n"
        debug_info += f"CfgPatches Class: {self.cfg_patches_class.get()}\n"
        debug_info += "Required Addons:\n"
        for addon in self.required_addons:
            debug_info += f"  - {addon.get()}\n"
        debug_info += f"Picture: {self.picture.get()}\n"
        debug_info += f"Drop Model: {self.drop_model.get()}\n"
        debug_info += f"CfgVehicles Uniform_base class: {self.cfg_vehicles_uniform_base_class.get()}\n"
        debug_info += f"Uniform Mother class: {self.uniform_mother_class.get()}\n"
        debug_info += f"Mother Model Path: {self.mother_model_path.get()}\n"
        debug_info += "Hidden Selections:\n"
        for selection in self.hidden_selections:
            debug_info += f"  - {selection.get()}\n"
        debug_info += "Hidden Textures:\n"
        for texture in self.hidden_textures:
            debug_info += f"  - {texture.get()}\n"
        debug_info += f"AceAx Model: {self.aceax_model.get()}\n"
        debug_info += f"AceAx Description: {self.aceax_description.get()}\n"
        debug_info += "AceAx Options:\n"
        for option in self.aceax_options:
            debug_info += f"  Option: {option['option'].get()}\n"
            debug_info += f"  Hidden Selection Number: {option['hidden_selection_number'].get()}\n"
            debug_info += "  Values:\n"
            for i, value in enumerate(option['values']):
                debug_info += f"    - Value: {value.get()}\n"
                debug_info += f"      Icon: {option['icons'][i].get()}\n"
                debug_info += f"      Texture: {option['textures'][i].get()}\n"
                debug_info += f"      Change Ingame: {option['change_ingame_vars'][i].get()}\n"
                debug_info += f"      Action Label: {option['action_labels'][i].get()}\n"

        debug_text.insert(tk.END, debug_info)

if __name__ == "__main__":
    root = tk.Tk()
    app = UniformConfigGenerator(root)
    root.mainloop()

