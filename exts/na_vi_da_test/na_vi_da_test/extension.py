import omni.ext
import omni.ui as ui
import omni.kit.commands
from pxr import Sdf,Usd


# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
def some_public_function(x: int):
    print("[na_vi_da_test] some_public_function was called with x: ", x)
    return x ** x

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class Na_vi_da_testExtension(omni.ext.IExt):
    
    
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[na_vi_da_test] na_vi_da_test startup")
        self.image_path = ""

        self._window = ui.Window("Textured Cube", width=300, height=200)
        with self._window.frame:
            with ui.VStack():
                label = ui.Label("hello")
                
                def click_spwan_cube():
                    self.spwan_cube()
                
                def click_load_image():
                    image_path = self.image_path.model.get_value_as_string()
                    print (f"load image: {image_path}")
                    

                    omni.kit.commands.execute('ChangeProperty',
                    prop_path=Sdf.Path('/World/Looks/OmniPBR/Shader.inputs:diffuse_texture'),
                    value=Sdf.AssetPath(image_path),
                    prev=None,
                    target_layer=Sdf.Find('anon:000001AB0879B400:World0.usd'),
                    usd_context_name=Usd.Stage.Open(rootLayer=Sdf.Find('anon:000001AB0879B400:World0.usd'), sessionLayer=Sdf.Find('anon:000001AB0879A5F0:World0-session.usda')))

                 
                def click_reset():
                    self.clear_all()

                with ui.HStack():
                    ui.Button("Spwan Cube", clicked_fn=click_spwan_cube)
                    ui.Button("Reset", clicked_fn=click_reset)
                
                with ui.HStack():
                    ui.Button("Load Image From Path", clicked_fn=click_load_image)
                with ui.HStack():
                    self.image_path = ui.StringField()
                    
    def spwan_cube(self):
        omni.kit.commands.execute('cl')
        self.cube = omni.kit.commands.execute('CreateMeshPrimWithDefaultXform',prim_type='Cube')[1]
        print("##########",self.cube)
    
        self.mat = omni.kit.commands.execute('CreateAndBindMdlMaterialFromLibrary',
            mdl_name='OmniPBR.mdl',
            mtl_name='OmniPBR',
            mtl_created_list=['/World/Looks/OmniPBR'],
            bind_selected_prims=[])
        
        print("##########",self.mat)

        omni.kit.commands.execute('BindMaterial',
            material_path='/World/Looks/OmniPBR',
            prim_path=['/World/Cube'],
            strength=['weakerThanDescendants'])
        
        print("Cube Spwaned")
        
    def clear_all(self)->None:

        omni.kit.commands.execute('DeletePrims',
            paths=[Sdf.Path('/World/Cube')],
            destructive=False)

        omni.kit.commands.execute('DeletePrims',
            paths=[Sdf.Path('/World/Looks')],
            destructive=False)
    
    def on_shutdown(self):
        print("[na_vi_da_test] na_vi_da_test shutdown")
