#!/bin/bash -e

# Global variables
ECO_PROFILE=~/.ecorithm_connect_profile
BASH_PROFILE=~/.bash_profile
LINE="source $ECO_PROFILE"
VARIABLES="
export ECO_CONNECT_USER=
export ECO_CONNECT_PASSWORD=

"



# Creating ecorithm_profile file
echo "Creating configuration file: $ECO_PROFILE"
echo "$VARIABLES" > "$ECO_PROFILE"
echo

# Setup eco logins
echo "Please enter your Ecorithm login information below."
read -p "User (Email or Username): " user
read -s -p "Password: " password
echo
echo
sed -i.bak "s~\(export ECO_CONNECT_USER*= *\).*~\1\"$user\"~" $ECO_PROFILE
sed -i.bak "s~\(export ECO_CONNECT_PASSWORD*= *\).*~\1\"$password\"~" $ECO_PROFILE


# Sourcing file in bash
echo "Setting configuration to $BASH_PROFILE..."
grep -q "$LINE" "$BASH_PROFILE" || echo "$LINE" >> "$BASH_PROFILE"
echo "Done."
echo
# All Good!
echo "You're all set! Enjoy the rest of your day :)"
