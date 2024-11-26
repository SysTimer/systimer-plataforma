import { Editor } from 'https://esm.sh/@tiptap/core@2.6.6';
import StarterKit from 'https://esm.sh/@tiptap/starter-kit@2.6.6';
import Image from 'https://esm.sh/@tiptap/extension-image@2.6.6';

window.addEventListener('load', function() {
    if (document.getElementById("wysiwyg-images-example")) {

    // tip tap editor setup
    const editor = new Editor({
        element: document.querySelector('#wysiwyg-images-example'),
        extensions: [
            StarterKit,
            Image
        ],
        content: '',
        editorProps: {
            attributes: {
                class: 'format lg:format-lg dark:format-invert focus:outline-none format-blue max-w-none',
            },
        }
    });

    // set up custom event listeners for the buttons
    document.getElementById('addImageButton').addEventListener('click', () => {
        const url = window.prompt('Enter image URL:', 'https://placehold.co/600x400');
        if (url) {
            editor.chain().focus().setImage({ src: url }).run();
        }
    });

    const advancedImageModal = FlowbiteInstances.getInstance('Modal', 'advanced-image-modal');
    
    document.getElementById('advancedImageForm').addEventListener('submit', (e) => {

        e.preventDefault();
        
        const imageUrl = document.getElementById('URL').value;
        const imageAlt = document.getElementById('alt').value;
        const imageTitle = document.getElementById('title').value;

        if (imageUrl) {
            editor.chain().focus().setImage({ src: imageUrl, alt: imageAlt ? imageAlt : '', title: imageTitle ? imageTitle: '' }).run();
            document.getElementById('advancedImageForm').reset();
            advancedImageModal.hide();
        }
    });
    
}
})

console.log('Olá mundo')