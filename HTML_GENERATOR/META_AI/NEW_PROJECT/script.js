document.addEventListener('DOMContentLoaded', () => {

    // Drawer variables
    const drawer = document.getElementById('drawer');
    let isDrawerOpen = false;
    
    // Theme toggle buttons and icon variable
    const darkModeOnIcon = "https://cdn-icons-png.flaticon.com/512/1249/1249564.png";
    const lightModeOnIcon = "https://assets.heweather.com/v2.0/moon.png";
    
    document.getElementById("moon-icon").src = lightModeOnIcon;
    
    // toggle theme function
    function toggleTheme() {
        const elementsList = ['drawer-toggle', 'toggle-text'];
        let toggleTextValue;
    
        elementsList.forEach(function (element) {
    
            document.getElementsByClassName(element)[0].classList.toggle('dark');
        })
    
        if (!isDrawerOpen)
          return;
        else {
          // Check on Dark Mode off
      console.log('Is Drawer Open:', isDrawerOpen)
    
    
              const icon = document.getElementById("moon-icon")
    console.log(icon.src,lightModeOnIcon)
              let toggleThemeVariable
    
    
    
              if(icon.src == darkModeOnIcon) {
                icon.src = lightModeOnIcon;
              } else {
                isDrawerOpen = false;
    
    icon.src=darkModeOnIcon ;
    
    const mainContent = document.getElementById('content');
    
    mainContent.textContent='Dark Mode ';
    
                    // Close the drawer when toggling theme
                    closeAllDrawers();
                    console.log('is Drawer Open:', isDrawerOpen);
              }
            if(icon.src == lightModeOnIcon) {
          icon.src=darkModeOn Icon;
    
            toggleThemeVariable=document.getElementById("moon-icon")
    }
        }
    
    }
    
    // closeAllDrawers function
    function closeAllDrawers() {
    
      // Check open flag & update content
       console.log(isDrawerOpen, "value check")
     console.info('drawer is currently' ,isDrawerOpen)
    
      const drawer = document.getElementById('drawer');
                const mainContent = document.getElementById('content');
            isDrawerOpen = false;
    
    mainContent.textContent='Main Drawer Content';
              // Update the state and show the close button
            updateDrawerStyles(isDrawerOpen);
        }
    // Drawer styles function to open & close drawwer and the update its style
    function updateDrawerStyles(show) {
    
      drawer.style.transform = show ? 'translateX(0px)' : 'translateX(-5000px)';
              drawer.classList.toggle('opened');
    
    let isOpenShowState = isDrawerOpen;
    
    
    if(!show && !isOpenShowState ) {
        // close the drawer,▕