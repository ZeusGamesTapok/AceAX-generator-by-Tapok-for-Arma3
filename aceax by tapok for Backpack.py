import tkinter as tk
from tkinter import ttk, messagebox
import itertools

class BackpackConfigGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Arma 3 Backpack Config Generator")
        self.master.geometry("1000x700")

        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.cfg_patches_frame = ttk.Frame(self.notebook)
        self.backpack_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.cfg_patches_frame, text="CfgPatches")
        self.notebook.add(self.backpack_frame, text="Backpack")

        self.create_cfg_patches_widgets()
        self.create_backpack_widgets()

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

    def create_backpack_widgets(self):
        self.backpack_canvas = tk.Canvas(self.backpack_frame)
        self.backpack_scrollbar = ttk.Scrollbar(self.backpack_frame, orient="vertical", command=self.backpack_canvas.yview)
        self.backpack_scrollable_frame = ttk.Frame(self.backpack_canvas)

        self.backpack_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.backpack_canvas.configure(
                scrollregion=self.backpack_canvas.bbox("all")
            )
        )

        self.backpack_canvas.create_window((0, 0), window=self.backpack_scrollable_frame, anchor="nw")
        self.backpack_canvas.configure(yscrollcommand=self.backpack_scrollbar.set)

        self.backpack_canvas.pack(side="left", fill="both", expand=True)
        self.backpack_scrollbar.pack(side="right", fill="y")

        self.create_cfg_vehicles_widgets()
        self.create_aceax_widgets()

    def create_cfg_vehicles_widgets(self):
        ttk.Label(self.backpack_scrollable_frame, text="CfgVehicles").pack(anchor='w', padx=10, pady=5)

        ttk.Label(self.backpack_scrollable_frame, text="Backpack Base Class:").pack(anchor='w', padx=10, pady=5)
        self.backpack_base_class = ttk.Entry(self.backpack_scrollable_frame)
        self.backpack_base_class.pack(fill=tk.X, padx=10, pady=5)
        self.backpack_base_class.insert(0, "CivilianBackpack")

        ttk.Label(self.backpack_scrollable_frame, text="Model:").pack(anchor='w', padx=10, pady=5)
        self.model = ttk.Entry(self.backpack_scrollable_frame)
        self.model.pack(fill=tk.X, padx=10, pady=5)
        self.model.insert(0, ".p3d")

        ttk.Label(self.backpack_scrollable_frame, text="Picture:").pack(anchor='w', padx=10, pady=5)
        self.picture = ttk.Entry(self.backpack_scrollable_frame)
        self.picture.pack(fill=tk.X, padx=10, pady=5)
        self.picture.insert(0, ".paa")

        ttk.Label(self.backpack_scrollable_frame, text="Mass:").pack(anchor='w', padx=10, pady=5)
        self.mass = ttk.Entry(self.backpack_scrollable_frame)
        self.mass.pack(fill=tk.X, padx=10, pady=5)
        self.mass.insert(0, "50")

        ttk.Label(self.backpack_scrollable_frame, text="Maximum Load:").pack(anchor='w', padx=10, pady=5)
        self.maximum_load = ttk.Entry(self.backpack_scrollable_frame)
        self.maximum_load.pack(fill=tk.X, padx=10, pady=5)
        self.maximum_load.insert(0, "240")

        self.hidden_selections_frame = ttk.Frame(self.backpack_scrollable_frame)
        self.hidden_selections_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(self.hidden_selections_frame, text="HiddenSelections:").pack(side=tk.LEFT)
        self.hidden_selections = []
        self.add_hidden_selection()

        ttk.Button(self.hidden_selections_frame, text="+", command=self.add_hidden_selection).pack(side=tk.LEFT)
        ttk.Button(self.hidden_selections_frame, text="-", command=self.remove_hidden_selection).pack(side=tk.LEFT)

        self.hidden_textures_frame = ttk.Frame(self.backpack_scrollable_frame)
        self.hidden_textures_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(self.hidden_textures_frame, text="HiddenTextures:").pack(side=tk.LEFT)
        self.hidden_textures = []
        self.add_hidden_texture()

        ttk.Button(self.hidden_textures_frame, text="+", command=self.add_hidden_texture).pack(side=tk.LEFT)
        ttk.Button(self.hidden_textures_frame, text="-", command=self.remove_hidden_texture).pack(side=tk.LEFT)

    def create_aceax_widgets(self):
        ttk.Label(self.backpack_scrollable_frame, text="AceAx").pack(anchor='w', padx=10, pady=5)

        ttk.Label(self.backpack_scrollable_frame, text="AceAx Model:").pack(anchor='w', padx=10, pady=5)
        self.aceax_model = ttk.Entry(self.backpack_scrollable_frame)
        self.aceax_model.pack(fill=tk.X, padx=10, pady=5)
        self.aceax_model.insert(0, "back")

        ttk.Label(self.backpack_scrollable_frame, text="AceAx Description:").pack(anchor='w', padx=10, pady=5)
        self.aceax_description = ttk.Entry(self.backpack_scrollable_frame)
        self.aceax_description.pack(fill=tk.X, padx=10, pady=5)
        self.aceax_description.insert(0, "backpack")

        self.aceax_options_frame = ttk.Frame(self.backpack_scrollable_frame)
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

        values_frame = ttk.Frame(option_frame)
        values_frame.pack(fill=tk.X)

        values = []
        icons = []
        textures = []

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

            ttk.Button(value_frame, text="-", command=lambda: remove_value(value_frame)).pack(side=tk.LEFT)

        def remove_value(value_frame):
            for i, frame in enumerate(values_frame.winfo_children()):
                if frame == value_frame:
                    if i < len(values):
                        values.pop(i)
                        icons.pop(i)
                        textures.pop(i)
                    value_frame.destroy()
                    break        

        ttk.Button(values_frame, text="+", command=add_value).pack()

        add_value()  # Add first value by default

        self.aceax_options.append({
            'option': option,
            'values': values,
            'icons': icons,
            'textures': textures
        })

    def generate_config(self):
        config = self.generate_cfg_patches()
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

    def generate_cfg_vehicles(self):
        cfg_vehicles = "class CfgVehicles\n{\n"
        cfg_vehicles += "    class Bag_Base;\n"
        cfg_vehicles += "    class Weapon_Bag_Base: Bag_Base\n    {\n"
        cfg_vehicles += "        class assembleInfo;\n"
        cfg_vehicles += "    };\n"
        cfg_vehicles += f"    class {self.backpack_base_class.get()} : Bag_Base\n    {{\n"
        cfg_vehicles += f'        author = "{self.author.get()}";\n'
        cfg_vehicles += "        scope=0;\n"
        cfg_vehicles += '        displayname = "This_IS_Hidden";\n'
        cfg_vehicles += f'        model = "{self.model.get()}";\n'
        cfg_vehicles += f'        picture = "{self.picture.get()}";\n'
        cfg_vehicles += f'        icon = "{self.picture.get()}";\n'
        cfg_vehicles += f'        mass = {self.mass.get()};\n'
        cfg_vehicles += f'        maximumLoad = {self.maximum_load.get()};\n'
        cfg_vehicles += "        hiddenSelections[] =\n        {\n"
        for selection in self.hidden_selections:
            cfg_vehicles += f'            "{selection.get()}",\n'
        cfg_vehicles = cfg_vehicles.rstrip(',\n') + "\n"
        cfg_vehicles += "        };\n"
        cfg_vehicles += "        hiddenSelectionsTextures[] =\n        {\n"
        for texture in self.hidden_textures:
            cfg_vehicles += f'            "{texture.get()}",\n'
        cfg_vehicles = cfg_vehicles.rstrip(',\n') + "\n"
        cfg_vehicles += "        };\n"
        cfg_vehicles += "    };\n"
        
        for variant in self.generate_backpack_variants():
            cfg_vehicles += self.generate_backpack_variant(variant)
        
        cfg_vehicles += "};\n\n"
        return cfg_vehicles

    def generate_backpack_variants(self):
        options = []
        for option in self.aceax_options:
            values = [value.get() for value in option['values'] if value.get()]
            if not values:
                print(f"Warning: No valid values for option {option['option'].get()}. Skipping this option.")
                continue
            options.append(values)
        return list(itertools.product(*options))

    def generate_backpack_variant(self, variant):
        variant_name = '_'.join(variant)
        backpack = f"    class {self.backpack_base_class.get()}_{variant_name} : {self.backpack_base_class.get()}\n    {{\n"
        backpack += "        scope=2;\n"
        backpack += f'        displayName="Backpack {variant_name}";\n'
        backpack += "        hiddenSelectionsTextures[] =\n        {\n"
        
        for i, option in enumerate(self.aceax_options):
            try:
                value_index = option['values'].index(next(v for v in option['values'] if v.get() == variant[i]))
                texture = option["textures"][value_index].get()
            except (ValueError, StopIteration):
                print(f"Warning: Value '{variant[i]}' not found in option {option['option'].get()}. Using default texture.")
                texture = option["textures"][0].get() if option["textures"] else ""
            
            backpack += f'            "{texture}",\n'
        
        backpack = backpack.rstrip(',\n') + "\n"
        backpack += "        };\n"
        backpack += "    };\n"
        return backpack

    def generate_xtd_gear_models(self):
        xtd_gear_models = "class XtdGearModels\n{\n"
        xtd_gear_models += "    class CfgVehicles\n    {\n"
        xtd_gear_models += f"        class {self.aceax_model.get()}\n        {{\n"
        xtd_gear_models += "            label = \"Backpack\";\n"
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
        xtd_gear_models += "    class CfgVehicles\n    {\n"
   
        for variant in self.generate_backpack_variants():
            xtd_gear_models += self.generate_xtd_gear_info(variant)
   
        xtd_gear_models += "    };\n"
        xtd_gear_models += "};\n"

        return xtd_gear_models

    def generate_xtd_gear_info(self, variant):
        variant_name = '_'.join(variant)
        info = f"        class {self.backpack_base_class.get()}_{variant_name}\n        {{\n"
        info += f'            model = "{self.aceax_model.get()}";\n'
   
        for i, option in enumerate(self.aceax_options):
            info += f'            {option["option"].get()} = "{variant[i]}";\n'
   
        info += "        };\n"
        return info

    def copy_to_clipboard(self, text):
        self.master.clipboard_clear()
        self.master.clipboard_append(text)
        messagebox.showinfo("Copied", "Config has been copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = BackpackConfigGenerator(root)
    root.mainloop()
