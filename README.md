# ComputerProject2021

# **Pong**
This is a clone of the game '*pong*'

# **Dependencies**
<ul>
    <h3>
    <li> python 3.8.5
    <li> tkinter
    <li> 
        PIL (v7.2.0)
        <pre><code>pip install pillow</code></pre> 
    </li>
    <li> 
        Montserrat (the font)
        The game still works but the text and labels will look bad 
    </li>
</ul>
    
# **Note**
For non windows machines comment out:
<ul>
    <li>
        line 7 in app.py 
        <pre><code>ctypes.windll.shcore.SetProcessDpiAwareness(1)</code></pre>
    </li>
    <li>
        line 16 in App/UI/Window.py 
        <pre><code>self._tkRoot.wm_attributes("-transparentcolor", "#000001")</code></pre>
    </li>
</ul>    



