"""
Script para generar iconos PWA de AgroDetect
Ejecutar: python generate_icons.py
"""

from PIL import Image
import os

def generate_icons():
    """Genera todos los iconos necesarios para PWA desde logo.png"""
    
    # Verificar que existe el logo
    if not os.path.exists('logo.png'):
        print("❌ Error: logo.png no encontrado")
        print("   Asegúrate de que logo.png esté en la misma carpeta")
        return
    
    print("🎨 Generando iconos PWA...")
    
    # Cargar logo original
    try:
        logo = Image.open('logo.png')
        print(f"✅ Logo cargado: {logo.size}")
    except Exception as e:
        print(f"❌ Error cargando logo: {e}")
        return
    
    # Crear carpeta para iconos
    icons_dir = 'icons'
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)
        print(f"📁 Carpeta '{icons_dir}' creada")
    
    # Tamaños necesarios para PWA
    sizes = {
        72: "Android (ldpi)",
        96: "Android (mdpi)",
        128: "Android (hdpi)",
        144: "Android (xhdpi)",
        152: "iOS",
        192: "Android (xxhdpi)",
        384: "Android (xxxhdpi)",
        512: "PWA Splash"
    }
    
    # Generar cada tamaño
    for size, description in sizes.items():
        try:
            # Redimensionar manteniendo calidad
            resized = logo.resize((size, size), Image.Resampling.LANCZOS)
            
            # Guardar en formato PNG
            output_path = os.path.join(icons_dir, f'icon-{size}x{size}.png')
            resized.save(output_path, 'PNG', optimize=True)
            
            print(f"✅ {size}x{size} creado ({description})")
            
        except Exception as e:
            print(f"❌ Error creando {size}x{size}: {e}")
    
    # Generar favicon.ico (múltiples tamaños)
    try:
        favicon_sizes = [(16, 16), (32, 32), (48, 48)]
        favicon_images = []
        
        for size in favicon_sizes:
            resized = logo.resize(size, Image.Resampling.LANCZOS)
            favicon_images.append(resized)
        
        favicon_images[0].save(
            'favicon.ico',
            format='ICO',
            sizes=[(16, 16), (32, 32), (48, 48)]
        )
        print("✅ favicon.ico creado (16x16, 32x32, 48x48)")
        
    except Exception as e:
        print(f"⚠️ No se pudo crear favicon.ico: {e}")
    
    # Generar apple-touch-icon (para iOS)
    try:
        apple_icon = logo.resize((180, 180), Image.Resampling.LANCZOS)
        apple_icon.save('apple-touch-icon.png', 'PNG', optimize=True)
        print("✅ apple-touch-icon.png creado (180x180)")
    except Exception as e:
        print(f"⚠️ No se pudo crear apple-touch-icon: {e}")
    
    print("\n" + "="*50)
    print("🎉 ¡Iconos generados exitosamente!")
    print("="*50)
    print(f"\n📁 Archivos creados en: ./{icons_dir}/")
    print("\n📋 Próximos pasos:")
    print("1. Copia el contenido de la carpeta 'icons' a tu proyecto")
    print("2. Actualiza manifest.json con las rutas correctas")
    print("3. Agrega <link rel='icon' href='favicon.ico'> en tu HTML")
    print("4. Agrega <link rel='apple-touch-icon' href='apple-touch-icon.png'>")


if __name__ == "__main__":
    generate_icons()
