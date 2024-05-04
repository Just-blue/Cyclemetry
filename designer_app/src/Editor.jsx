import React, { useEffect, useRef } from "react";
import { JSONEditor } from "@json-editor/json-editor";
import axios from "axios";

function Editor() {
  const config = {
    use_name_attributes: false,
    theme: "bootstrap4",
    disable_edit_json: true,
    disable_properties: true,
    disable_collapse: true,
    schema: {
      title: "Person",
      type: "object",
      required: [
        "name",
        "age",
        "date",
        "favorite_color",
        "gender",
        "location",
        "pets",
      ],
      properties: {
        name: {
          type: "string",
          description: "First and Last name",
          minLength: 4,
          default: "Jeremy Dorn",
        },
        age: {
          type: "integer",
          default: 25,
          minimum: 18,
          maximum: 99,
        },
        favorite_color: {
          type: "string",
          format: "color",
          title: "favorite color",
          default: "#ffa500",
        },
        gender: {
          type: "string",
          enum: ["male", "female", "other"],
        },
        date: {
          type: "string",
          format: "date",
          options: {
            flatpickr: {},
          },
        },
        location: {
          type: "object",
          title: "Location",
          properties: {
            city: {
              type: "string",
              default: "San Francisco",
            },
            state: {
              type: "string",
              default: "CA",
            },
            citystate: {
              type: "string",
              description:
                "This is generated automatically from the previous two fields",
              template: "{{city}}, {{state}}",
              watch: {
                city: "location.city",
                state: "location.state",
              },
            },
          },
        },
        pets: {
          type: "array",
          format: "table",
          title: "Pets",
          uniqueItems: true,
          items: {
            type: "object",
            title: "Pet",
            properties: {
              type: {
                type: "string",
                enum: ["cat", "dog", "bird", "reptile", "other"],
                default: "dog",
              },
              name: {
                type: "string",
              },
            },
          },
          default: [
            {
              type: "dog",
              name: "Walter",
            },
          ],
        },
      },
    },
  };

  const editorRef = useRef(null);

  const postData = {};

  const generateDemoFrame = async () => {
    console.log("sending req");
    try {
      const response = await axios.post("http://localhost:8080/demo", postData);
      console.log("Response:", response.data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  useEffect(() => {
    const editor = new JSONEditor(editorRef.current, config);
    editor.on("change", function () {
      generateDemoFrame();

      // TODO trigger image generation - in backend
      // document.querySelector('#input').value = JSON.stringify(editor.getValue())
    });
    return () => {
      editor.destroy(); // Destroy the JSONEditor instance when component unmounts
    };
  }, []); // Empty dependency array to run the effect only once after the initial render

  return <div ref={editorRef} />;
}

export default Editor;
