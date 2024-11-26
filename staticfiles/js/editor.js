import { Editor } from '@tiptap/core';
import StarterKit from '@tiptap/starter-kit';
import TextAlign from '@tiptap/extension-text-align';


console.log('Olá entrou aqui.')

window.addEventListener('load', function() {
    if (document.getElementById("wysiwyg-images-example")) {

    // tip tap editor setup
    const editor = new Editor({
        element: document.querySelector('#wysiwyg-images-example'),
        extensions: [
            StarterKit,
            Image
        ],
        content: '<p>Flowbite is an <strong>open-source library of UI components</strong> based on the utility-first Tailwind CSS framework featuring dark mode support, a Figma design system, and more.</p><img src="https://placehold.co/600x400" contenteditable="false" draggable="true"><p>It includes all of the commonly used components that a website requires, such as buttons, dropdowns, navigation bars, modals, datepickers, advanced charts and the list goes on.</p><p>Here is an example of a button component:</p><code>&#x3C;button type=&#x22;button&#x22; class=&#x22;text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800&#x22;&#x3E;Default&#x3C;/button&#x3E;</code><p>Learn more about all components from the <a href="https://flowbite.com/docs/getting-started/introduction/">Flowbite Docs</a>.</p>',
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