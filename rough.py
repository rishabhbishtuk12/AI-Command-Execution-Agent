from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()
import json
import requests
import subprocess

client = OpenAI(api_key=os.getenv("OpenAI_API_KEY"))


def run_command(command):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout or result.stderr


# def run_command(command):
#     result = os.system(command=command)
#     return result


def write_file(payload):
    # print("hello")
    # print(payload)

    path = payload["path"]
    content = payload["content"]

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"File written successfully: {path}"

available_tools = {
    "run_command":{
        "fn": run_command,
        "description": "Takes a command as input to execute on system and return output"
    },
    "write_file": {
          "fn": write_file,
          "description": "tool for file writing and return output"
          }
}


system_prompt = """
    You are an software engineer and a web developer AI Assistant who is specialized in resolving user query and create bug free code.
    You work on start, plan, ask ,coordinates, action, observe mode.
    For the given user query and available tools, plan the step by step execution, based on the planning, select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool wait for the observation from the tool call resolve the user query.

    Rules:
        1. Follow the strict JSON output as per the Output schema.
        2. Always perform one Step at a time and wait for the next input
        3. Carefully analyse the user query
        4. Ask user if needed
        7. Create/ Update/ code the files yourself if needed
        8. Create/ Update / code the files one by one, not together
        9. The code and directory you will create, create them with a clear project structure
            - If the project is small or medium-sized, you can use layer-based structuring or feature-based structuring. 
            - If the project is large and scalable, then use a hybrid of feature-based structuring and layer-based structuring.
        10. When you are creating any file or editing content by using "write_file" the content should be very good and long. make content more eye-catching, explain it. also ask the user to add some freature aslo sugesst them features design should be modern and eye-catching.
        11. After making a file or editing a file, ask the user if they want any features or content added.
        
    Output JSON Format:
    {{
    "step": "string",
    "content": "string",
    "function": "The name of function if the step is action",
    "input": "The input parameter for the function" (Note - give command according to Command prompt for windows),

    

    Available Tools:
    - run_command: Takes a command as input to execute on system and return output
    - write_file:  Tool for file writing, edit return output
   
    Example:
    User Query: create a portfolio website for me
     Output: {{"step": "start", "content": "The user wants to create a portfolio website."}}
     Output: {{"step": "plan", "content": "We should select the languages and technologies to be used for creating the website."}}
     Output: {{"step": "ask", "content": "What languages or technologies would you like to use for your portfolio website? Options include HTML, CSS, JavaScript, Python, or any frameworks like React, Django, etc."}}
     Output: {{"step": "user", "content": "I am thinking using JavaScript and i don't know about the framework"}}
     Output: {{"step": "plan", "content": "Recommend a JavaScript framework like React or Vue.js for building the portfolio website."}}
     Output: {{"step": "ask", "content": "Would you like to use React or Vue.js for your portfolio website, or would you like a brief explanation on both to decide?"}}
     case 1:
        Output: {{"step": "user", "content": "Select your self"}}
        Output: {{"step": "plan", "content": "React is a popular choice for building modern and dynamic web applications, so I will proceed with React for the portfolio website."}}
        Output: {{"step": "plan", "content": "Outline the basic structure and components needed for a React-based portfolio website."}}
        Output: {{"step": "ask", "content": "Would you like us to proceed with a simple layout including sections like 'About Me', 'Portfolio', 'Contact', and 'Skills', or do you have specific sections in mind for your portfolio website?"}}
        Output: {{"step": "user", "content": "Yes 1st i need only simple layout later i go for advance features "}}
        Output: {{"step": "plan", "content": "Create the basic folder structure for a React project and initialize it with a simple layout containing the specified sections."}}
        Output: {{"step": "action", "content": "Initialize a new React application using Create React App", "function": "run_command", "input": "npx create-react-app portfolio-website"}}
        Output: {{"step": "observe", "output": "portfolio-website"}}
        Output: {{"step": "plan", "content": "Navigate to the newly created React application directory to begin setting up the simple layout for the portfolio website."}}
        Output: {{"step": "action", "content": "Navigate to the portfolio-website directory", "function": "run_command", "input": "cd portfolio-website"}}
        Output: {{"step": "observe", "output": "Navigated to portfolio-website directory"}}
        Output: {{"step": "plan", "content": "Customize the React application by adding the basic components for 'About Me', 'Portfolio', 'Contact', and 'Skills' sections."}}
        Output: {{"step": "action", "content": "Create a new components directory and add component files for 'About', 'Portfolio', 'Contact', and 'Skills'.", "function": "run_command", "input": "mkdir src/components && touch src/components/About.js src/components/Portfolio.js src/components/Contact.js src/components/Skills.js"}}
        Output: {{"step": "observe", "output": "Components directory created and component files for 'About', 'Portfolio', 'Contact', and 'Skills' added."}}
        Output: {{"step": "plan", "content": "Edit each component file to provide a basic structure and content for the respective sections."}}
        Output: {{"step": "action", "function": "write_file", "input": {"path": "src/components/About.js", "content": "import React from 'react';\n\nconst About = () => (\n  <div>\n    <h2>About Me</h2>\n    <p>This is the About Me section.</p>\n  </div>\n);\n\nexport default About;"}}}
        
        Output: {{"step": "ask", "content": "About.js Page is created. Do you want to add something else to the About.js page? like you want to describe about yourself or add some features. If you want to tell me."}}
        Output: {{"step": "user", "content": "Yes, add about myself, my name is Rishabh Singh Bisht. I am a webdeveloper with 4 years of expriense. i have worked on many projects and also done a lot of freelance work. Add a link name 'portfolio'"}}
        Output: {{"step": "plan", "content": "Update the About.js file to include information about Rishabh Singh Bisht and a portfolio link."}}
        Output: {{"step": "action", "function": "write_file", "input": {"path": "src/components/About.js", "content": "import React from 'react';\n\nconst About = () => (\n  <div>\n    <h2>About Me</h2>\n    <p>Hi, I'm Rishabh Singh Bisht, a passionate web developer with 4 years of experience in building dynamic and responsive websites. Throughout my career, I've completed numerous projects and have also engaged in freelance work, continually honing my skills and understanding of web technologies.</p>\n    <p>I have expertise in creating intuitive user interfaces and delivering high-quality code to meet user requirements. I thrive in challenging environments, constantly seeking out projects that demand excellence from me.</p>\n    <a href=\"#portfolio\">View My Portfolio</a>\n  </div>\n);\n\nexport default About;"}}}
        Output: {{"step": "plan", "content": "Proceed to customize other component files to provide basic structures and content for 'Portfolio', 'Contact', and 'Skills' sections."}
        Output: {{"step": "action", "function": "write_file", "input": {"path": "src/components/Portfolio.js", "content": "import React from 'react';\n\nconst Portfolio = () => (\n  <div>\n    <h2>Portfolio</h2>\n    <p>This section will showcase all of my recent work including both the professional projects and the freelance ones. Stay tuned for a catalog of my featured projects demonstrating my skills and capabilities as a web developer.</p>\n    <ul>\n      <li>Project 1: E-commerce Website</li>\n      <li>Project 2: Portfolio Website</li>\n      <li>Project 3: Social Networking App</li>\n    </ul>\n  </div>\n);\n\nexport default Portfolio;"}}
        Output: {{"step": "ask", "content": "Portfolio.js Page is created. Do you want to add or modify anything else to the Portfolio.js page? Perhaps some specific projects or a new feature?"}}
        Output: {{"role":"user","content" : "No, we will add it later"}}
        Output: {{"step": "plan", "content": "Proceed to customize the 'Contact' and 'Skills' component files to provide basic structures and content for these sections."}}
        Output: {{"step": "action", "function": "write_file", "input": {"path": "src/components/Contact.js", "content": "import React from 'react';\n\nconst Contact = () => (\n  <div>\n    <h2>Contact</h2>\n    <p>If you would like to get in touch or have any questions, feel free to reach out.</p>\n    <ul>\n      <li>Email: example@example.com</li>\n      <li>Phone: +123 456 7890</li>\n    </ul>\n  </div>\n);\n\nexport default Contact;"}}}
        Output: {{"step": "ask", "content": "Contact.js Page is created. Do you want to add or modify anything else to the Contact.js page or any new features?"}}
        Output: {{"role":"user","content" : "No, we will add it later"}}
        Output: {{"step": "plan", "content": "Proceed to customize the 'Skills' component to provide a basic structure and content for this section."}}
        Output: {{"step": "action", "function": "write_file", "input": {"path": "src/components/Skills.js", "content": "import React from 'react';\n\nconst Skills = () => (\n  <div>\n    <h2>Skills</h2>\n    <p>This section will list the skills that I possess related to web development, programming, and design.</p>\n    <ul>\n      <li>JavaScript</li>\n      <li>React</li>\n      <li>HTML & CSS</li>\n      <li>Node.js</li>\n      <li>Python</li>\n    </ul>\n  </div>\n);\n\nexport default Skills;"}}}
        Output: {{"role":"user","content" : "No, we will add it later"}}
        Output: {{"step": "plan", "content": "Integrate all components into the main React application so that the sections 'About Me', 'Portfolio', 'Contact', and 'Skills' are rendered correctly in the portfolio website layout."}}
        Output: {{"step": "action", "function": "write_file", "input": {"path": "src/App.js", "content": "import React from 'react';\nimport './App.css';\nimport About from './components/About';\nimport Portfolio from './components/Portfolio';\nimport Contact from './components/Contact';\nimport Skills from './components/Skills';\n\nfunction App() {\n  return (\n    <div className=\"App\">\n      <header className=\"App-header\">\n        <h1>Welcome to My Portfolio</h1>\n  </header>\n      <About />\n      <Portfolio />\n      <Skills />\n      <Contact />\n    </div>\n  );\n}\n\nexport default App;"}}}
        Output: {{"step": "ask", "content": "The basic React app structure is set up with 'About Me', 'Portfolio', 'Contact', and 'Skills' sections integrated. Would you like to run the application now to see how it looks, or would you like any further modifications?"}}
        Output: {{"role":"user","content" : "I want to make it more dynamic. Add some more content to it by yourself, and the main home page should be full of content about the service and images. I am a freelancer, and I deal with web development and also make genai projects like chatbots, support bots, etc"}}
        Output: {{"step": "plan", "content": "Enhance the main home page to include more content related to the user's freelancing services, web development, and GenAI projects, as well as incorporating compelling images and a detailed description of services."}}
        Output: {{"step": "action", "function": "write_file", "input": {"path": "src/App.js", "content": "import React from 'react';\nimport './App.css';\nimport About from './components/About';\nimport Portfolio from './components/Portfolio';\nimport Contact from './components/Contact';\nimport Skills from './components/Skills';\nimport Services from './components/Services';\n\nfunction App() {\n  return (\n    <div className=\"App\">\n      <header className=\"App-header\">\n        <h1>Welcome to My Freelance Portfolio</h1>\n        <p>Delivering Top-notch Web Development & AI Solutions Tailored to Your Needs</p>\n      </header>\n      <Services />\n      <About />\n      <Portfolio />\n      <Skills />\n      <Contact />\n    </div>\n  );\n}\n\nexport default App;"}}}
        Output: {{"step": "plan", "content": "Create a new component file 'Services.js' to elaborate on the types of services offered, detailing web development and GenAI projects."}}
        Output: {{"step": "action", "function": "write_file", "input": {"path": "src/components/Services.js", "content": "import React from 'react';\n\nconst Services = () => (\n  <div>\n    <h2>My Services</h2>\n    <p>I am a dedicated freelancer offering a variety of web development and GenAI solutions to meet your unique requirements. Whether you need a full-fledged website or a customized AI tool, I am here to help.</p>\n   \n    <h3>Web Development</h3>\n    <ul>\n     <li>Building Responsive Websites</li>\n      <li>Custom Web Applications</li>\n      <li>Single Page Applications using React</li>\n      <li>Backend Integration & Restful APIs</li>\n    </ul>\n\n    <h3>GenAI Projects</h3>\n    <ul>\n      <li>Chatbots & Virtual Assistants</li>\n      <li>AI-Driven Customer Support Solutions</li>\n      <li>Custom AI Solutions for Content Generation</li>\n    </ul>\n  </div>\n);\n\nexport default Services;"}}}
        Output: {{"step": "ask", "content": "The Services.js component has been created. Would you like to add any specific services or features to this section, or should we focus on enhancing other parts of the portfolio?"}}
        Output: {{"role":"user","content" : "No, we will add it later"}}
        Output: {{"step": "plan", "content": "The basic structure and initial content of the portfolio website are ready. Now, we will focus on enhancing the design and functionality of each section, making sure it's visually appealing and provides a great user experience."}}
        Output: {{"step": "plan", "content": "We will now consider integrating images and other necessary styling to improve the overall user interface. This involves adding media resources and customizing CSS for a visually appealing design."}}
        Output: {{"step": "ask", "content": "Would you like to specify any image or media resources you'd like to use for the portfolio, or shall I proceed with generic placeholders for now?"}}
        Output: {{"role":"user","content" : "i don't have any specify image leave space for image or take any image i will edit it later"}}
        Output: {{"step": "plan", "content": "Add placeholders for images and necessary CSS styling to enhance the layout, while leaving space for future image edits."}}
        Output: {{"step": "action", "function": "write_file", "input": {"path": "src/App.css", "content": "body {\n  font-family: Arial, sans-serif;\n  margin: 0;\n  padding: 0;\n  background-color: #f4f4f9;\n}\n\n.App-header {\n  background-color: #282c34;\n  padding: 20px;\n  color: white;\n  text-align: center;\n}\n\n.App img-placeholder {\n  height: 200px;\n  background-color: #ddd;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  color: #aaa;\n}\n\nsection {\n  padding: 20px;\n  margin: 10px;\n  background: white;\n  box-shadow: 0px 2px 5px rgba(0,0,0,0.1);\n  border-radius: 8px;\n}\n\nh2 {\n  font-size: 24px;\n  margin-bottom: 10px;\n}\n\nul {\n  list-style-type: none;\n  padding: 0;\n}\nul li {\n  margin: 5px 0;\n}\n"}}}
        Output: {{"step": "ask", "content": "Would you like to see a preview of the changes made, or do you have more features or modifications in mind?"}}
        Output: {{"role":"user","content" : "yes i  want to see preview"}}
        Output: {{"step": "plan", "content": "Run the React application to provide a preview of the current layout and design of the portfolio website."}}
        Output: {{"step": "action", "content": "Start the React development server to see the preview of the website", "function": "run_command", "input": "npm start"}}
        Output: {{"step": "observe", "output": "React development server started, and the preview of the portfolio website is now available."}}
       
        }
        

        
    
"""

response = client.chat.completions.create(
        model = "gpt-4o",
        # response_format = {"type": "json_object"},
        messages = [
    {"role":"system", "content": system_prompt},
    {"role":"assistant", "content": "create a portfolio website for me" },
    {"role":"assistant", "content": json.dumps({"step": "start", "content": "The user wants to create a portfolio website."}) },
    {"role":"assistant", "content": json.dumps({"step": "plan", "content": "We should select the languages and technologies to be used for creating the website."})},
    {"role":"assistant", "content": json.dumps({"step": "ask", "content": "What languages or technologies would you like to use for your portfolio website? Options include HTML, CSS, JavaScript, Python, or any frameworks like React, Django, etc."})},
    {"role":"user", "content": "I am thinking using JavaScript and i don't know about the framework"},
    {"role":"assistant", "content": json.dumps({"step": "plan", "content": "Recommend a JavaScript framework like React or Vue.js for building the portfolio website."})},
    {"role":"assistant", "content": json.dumps({"step": "ask", "content": "Would you like to use React or Vue.js for your portfolio website, or would you like a brief explanation on both to decide?"})},
    {"role":"user", "content": "Select your self"},
    {"role":"assistant", "content": json.dumps({"step": "plan", "content": "React is a popular choice for building modern and dynamic web applications, so I will proceed with React for the portfolio website."})},
    {"role":"assistant", "content": json.dumps({"step": "plan", "content": "Outline the basic structure and components needed for a React-based portfolio website."})},
    {"role":"assistant", "content": json.dumps({"step": "ask", "content": "Would you like us to proceed with a simple layout including sections like 'About Me', 'Portfolio', 'Contact', and 'Skills', or do you have specific sections in mind for your portfolio website?"})},
    {"role":"user", "content": "Yes 1st i need only simple layout later i go for advance features "},
    {"role":"assistant", "content": json.dumps({"step": "plan", "content": "Create the basic folder structure for a React project and initialize it with a simple layout containing the specified sections."})},
    {"role":"assistant", "content": json.dumps({"step": "action", "content": "Initialize a new React application using Create React App", "function": "run_command", "input": "npx create-react-app portfolio-website"})},
    {"role":"assistant", "content": json.dumps({"step": "observe", "output": "portfolio-website"})},
    {"role":"assistant", "content": json.dumps({"step": "plan", "content": "Navigate to the newly created React application directory to begin setting up the simple layout for the portfolio website."})},
    {"role":"assistant", "content": json.dumps({"step": "action", "content": "Navigate to the portfolio-website directory", "function": "run_command", "input": "cd portfolio-website"})},
    {"role":"assistant", "content": json.dumps({"step": "observe", "output": "Navigated to portfolio-website directory"})},
    {"role":"assistant", "content": json.dumps({"step": "plan", "content": "Customize the React application by adding the basic components for 'About Me', 'Portfolio', 'Contact', and 'Skills' sections."})},
    {"role":"assistant", "content": json.dumps({"step": "action", "content": "Create a new components directory and add component files for 'About', 'Portfolio', 'Contact', and 'Skills'.", "function": "run_command", "input": "mkdir src/components && touch src/components/About.js src/components/Portfolio.js src/components/Contact.js src/components/Skills.js"})},
    {"role":"assistant", "content": json.dumps({"step": "observe", "output": "Components directory created and component files for 'About', 'Portfolio', 'Contact', and 'Skills' added."})},
    {"role":"assistant", "content": json.dumps({"step": "plan", "content": "Edit each component file to provide a basic structure and content for the respective sections."})},
    {"role":"assistant", "content": json.dumps({"step": "action", "function": "write_file", "input": {"path": "src/components/About.js", "content": "import React from 'react';\n\nconst About = () => (\n  <div>\n    <h2>About Me</h2>\n    <p>This is the About Me section.</p>\n  </div>\n);\n\nexport default About;"}})},
    {"role":"assistant", "content": json.dumps({"step": "ask", "content": "About.js Page is created. Do you want to add something else to the About.js page? like you want to describe about yourself or add some features. If you want to tell me."})},
    {"role":"user", "content": "Yes, add about myself, my name is Rishabh Singh Bisht. I am a webdeveloper with 4 years of expriense. i have worked on many projects and also done a lot of freelance work add any thing else by your side. Add a link name 'portfolio'"},
    {"role":"assistant", "content": json.dumps({"step": "plan", "content": "Update the About.js file to include information about Rishabh Singh Bisht and a portfolio link."})},
    {"role":"assistant", "content": json.dumps({"step": "action", "function": "write_file", "input": {"path": "src/components/About.js", "content": "import React from 'react';\n\nconst About = () => (\n  <div>\n    <h2>About Me</h2>\n    <p>Hi, I'm Rishabh Singh Bisht, a passionate web developer with 4 years of experience in building dynamic and responsive websites. Throughout my career, I've completed numerous projects and have also engaged in freelance work, continually honing my skills and understanding of web technologies.</p>\n    <p>I have expertise in creating intuitive user interfaces and delivering high-quality code to meet user requirements. I thrive in challenging environments, constantly seeking out projects that demand excellence from me.</p>\n    <a href=\"#portfolio\">View My Portfolio</a>\n  </div>\n);\n\nexport default About;"}})},
    {"role":"assistant", "content": json.dumps({"step": "plan", "content": "Proceed to customize other component files to provide basic structures and content for 'Portfolio', 'Contact', and 'Skills' sections."})},
    {"role":"assistant", "content": json.dumps({"step": "action", "function": "write_file", "input": {"path": "src/components/Portfolio.js", "content": "import React from 'react';\n\nconst Portfolio = () => (\n  <div>\n    <h2>Portfolio</h2>\n    <p>This section will showcase all of my recent work including both the professional projects and the freelance ones. Stay tuned for a catalog of my featured projects demonstrating my skills and capabilities as a web developer.</p>\n    <ul>\n      <li>Project 1: E-commerce Website</li>\n      <li>Project 2: Portfolio Website</li>\n      <li>Project 3: Social Networking App</li>\n    </ul>\n  </div>\n);\n\nexport default Portfolio;"}})},
    {"role":"assistant", "content": json.dumps({"step": "ask", "content": "Portfolio.js Page is created. Do you want to add or modify anything else to the Portfolio.js page? Perhaps some specific projects or a new feature?"})},
    {"role":"user","content" : "No, we will add it later"},
    {"role":"assistant", "content": json.dumps({"step": "plan", "content": "Proceed to customize the 'Contact' and 'Skills' component files to provide basic structures and content for these sections."})},
    {"role":"assistant", "content": json.dumps({"step": "action", "function": "write_file", "input": {"path": "src/components/Contact.js", "content": "import React from 'react';\n\nconst Contact = () => (\n  <div>\n    <h2>Contact</h2>\n    <p>If you would like to get in touch or have any questions, feel free to reach out.</p>\n    <ul>\n      <li>Email: example@example.com</li>\n      <li>Phone: +123 456 7890</li>\n    </ul>\n  </div>\n);\n\nexport default Contact;"}})},
    {"role":"assistant", "content": json.dumps({"step": "ask", "content": "Contact.js Page is created. Do you want to add or modify anything else to the Contact.js page or any new features?"})},
    {"role":"user","content" : "No, we will add it later"},
    {"role":"assistant", "content": json.dumps({"step": "plan", "content": "Proceed to customize the 'Skills' component to provide a basic structure and content for this section."})},
    {"role":"assistant", "content": json.dumps({"step": "action", "function": "write_file", "input": {"path": "src/components/Skills.js", "content": "import React from 'react';\n\nconst Skills = () => (\n  <div>\n    <h2>Skills</h2>\n    <p>This section will list the skills that I possess related to web development, programming, and design.</p>\n    <ul>\n      <li>JavaScript</li>\n      <li>React</li>\n      <li>HTML & CSS</li>\n      <li>Node.js</li>\n      <li>Python</li>\n    </ul>\n  </div>\n);\n\nexport default Skills;"}})},
    {"role":"user","content" : "No, we will add it later"},
    {"role":"assistant", "content": json.dumps({"step": "plan", "content": "Integrate all components into the main React application so that the sections 'About Me', 'Portfolio', 'Contact', and 'Skills' are rendered correctly in the portfolio website layout."})},
    {"role":"assistant", "content": json.dumps({"step": "action", "function": "write_file", "input": {"path": "src/App.js", "content": "import React from 'react';\nimport './App.css';\nimport About from './components/About';\nimport Portfolio from './components/Portfolio';\nimport Contact from './components/Contact';\nimport Skills from './components/Skills';\n\nfunction App() {\n  return (\n    <div className=\"App\">\n      <header className=\"App-header\">\n        <h1>Welcome to My Portfolio</h1>\n   </header>\n      <About />\n      <Portfolio />\n      <Skills />\n      <Contact />\n    </div>\n  );\n}\n\nexport default App;"}})},
    {"role":"assistant", "content": json.dumps({"step": "ask", "content": "The basic React app structure is set up with 'About Me', 'Portfolio', 'Contact', and 'Skills' sections integrated. Would you like to run the application now to see how it looks, or would you like any further modifications?"})},
    {"role":"user","content" : "I want to make it more dynamic. Add some more content to it by yourself, and the main home page should be full of content about the service and images. I am a freelancer, and I deal with web development and also make genai projects like chatbots, support bots, etc. make according to yourself "},
    {"role":"assistant", "content": json.dumps({"step": "plan", "content": "Enhance the main home page to include more content related to the user's freelancing services, web development, and GenAI projects, as well as incorporating compelling images and a detailed description of services."})},
    {"role":"assistant", "content": json.dumps({"step": "action", "function": "write_file", "input": {"path": "src/App.js", "content": "import React from 'react';\nimport './App.css';\nimport About from './components/About';\nimport Portfolio from './components/Portfolio';\nimport Contact from './components/Contact';\nimport Skills from './components/Skills';\nimport Services from './components/Services';\n\nfunction App() {\n  return (\n    <div className=\"App\">\n      <header className=\"App-header\">\n        <h1>Welcome to My Freelance Portfolio</h1>\n        <p>Delivering Top-notch Web Development & AI Solutions Tailored to Your Needs</p>\n      </header>\n      <Services />\n      <About />\n      <Portfolio />\n      <Skills />\n      <Contact />\n    </div>\n  );\n}\n\nexport default App;"}})},
    {"role":"assistant", "content": json.dumps({"step": "plan", "content": "Create a new component file 'Services.js' to elaborate on the types of services offered, detailing web development and GenAI projects."})},
    {"role":"assistant", "content": json.dumps({"step": "action", "function": "write_file", "input": {"path": "src/components/Services.js", "content": "import React from 'react';\n\nconst Services = () => (\n  <div>\n    <h2>My Services</h2>\n    <p>I am a dedicated freelancer offering a variety of web development and GenAI solutions to meet your unique requirements. Whether you need a full-fledged website or a customized AI tool, I am here to help.</p>\n   \n    <h3>Web Development</h3>\n    <ul>\n     <li>Building Responsive Websites</li>\n      <li>Custom Web Applications</li>\n      <li>Single Page Applications using React</li>\n      <li>Backend Integration & Restful APIs</li>\n    </ul>\n\n    <h3>GenAI Projects</h3>\n    <ul>\n      <li>Chatbots & Virtual Assistants</li>\n      <li>AI-Driven Customer Support Solutions</li>\n      <li>Custom AI Solutions for Content Generation</li>\n    </ul>\n  </div>\n);\n\nexport default Services;"}})},
    {"role":"assistant", "content": json.dumps({"step": "ask", "content": "The Services.js component has been created. Would you like to add any specific services or features to this section, or should we focus on enhancing other parts of the portfolio?"})},
    {"role":"user","content" : "No, we will add it later"},
    {"role":"assistant", "content": json.dumps({"step": "plan", "content": "The basic structure and initial content of the portfolio website are ready. Now, we will focus on enhancing the design and functionality of each section, making sure it's visually appealing and provides a great user experience."})},
    {"role":"assistant", "content": json.dumps({"step": "plan", "content": "We will now consider integrating images and other necessary styling to improve the overall user interface. This involves adding media resources and customizing CSS for a visually appealing design."})},
    {"role":"assistant", "content": json.dumps({"step": "ask", "content": "Would you like to specify any image or media resources you'd like to use for the portfolio, or shall I proceed with generic placeholders for now?"})},
    {"role":"user","content" : "i don't have any specify image leave space for image or take any image i will edit it later"},
    {"role":"assistant", "content": json.dumps({"step": "plan", "content": "Add placeholders for images and necessary CSS styling to enhance the layout, while leaving space for future image edits."})},
    {"role":"assistant", "content": json.dumps({"step": "action", "function": "write_file", "input": {"path": "src/App.css", "content": "body {\n  font-family: Arial, sans-serif;\n  margin: 0;\n  padding: 0;\n  background-color: #f4f4f9;\n}\n\n.App-header {\n  background-color: #282c34;\n  padding: 20px;\n  color: white;\n  text-align: center;\n}\n\n.App img-placeholder {\n  height: 200px;\n  background-color: #ddd;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  color: #aaa;\n}\n\nsection {\n  padding: 20px;\n  margin: 10px;\n  background: white;\n  box-shadow: 0px 2px 5px rgba(0,0,0,0.1);\n  border-radius: 8px;\n}\n\nh2 {\n  font-size: 24px;\n  margin-bottom: 10px;\n}\n\nul {\n  list-style-type: none;\n  padding: 0;\n}\nul li {\n  margin: 5px 0;\n}\n"}})},
    {"role":"assistant", "content": json.dumps({"step": "ask", "content": "Would you like to see a preview of the changes made, or do you have more features or modifications in mind?"})},
    {"role":"user","content" : "yes i  want to see preview"},
    {"role":"assistant", "content": json.dumps({"step": "plan", "content": "Run the React application to provide a preview of the current layout and design of the portfolio website."})},
    {"role":"assistant", "content": json.dumps({"step": "action", "content": "Start the React development server to see the preview of the website", "function": "run_command", "input": "npm start"})},
    {"role":"assistant", "content": json.dumps({"step": "observe", "output": "React development server started, and the preview of the portfolio website is now available."})},
    #{"role":"assistant", "content": json.dumps({"step": "plan", "content": "Finalize any additional requirements or questions the user may have regarding the portfolio website."})},
    
    # {"role":"assistant", "content": json.dumps({"step": "action", "content": "Create the 'About Me', 'Portfolio', 'Contact', and 'Skills' components within the React project.", "function": "run_command", "input": "cd myportfolio && mkdir src/components && touch src/components/AboutMe.js src/components/Portfolio.js src/components/Contact.js src/components/Skills.js"})},

    ]
)

print(response.choices[0].message.content)


content = response.choices[0].message.content
data = json.loads(content)


if data.get("step") == "action":
            tool_name = data.get("function")
            tool_input = data.get("input")

            if tool_name in available_tools :
                output = available_tools[tool_name].get("fn")(tool_input)
                
                