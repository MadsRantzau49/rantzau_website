import os
import json

def get_player_data_html():
    print(f"                     d                  d                     d {os.getcwd()}")
    html_file_path = "C:/Users/madsr/Documents/code/rantzau_website/websites/OB_Boedekasse/public/index.html"
    player_data_path = "C:/Users/madsr/Documents/code/rantzau_website/websites/OB_Boedekasse/database/player_finance.json"

    # Check if index.html exists
    if not os.path.exists(html_file_path):
        raise FileNotFoundError(f"{html_file_path} not found!")

    # Read the existing index.html content
    with open(html_file_path, 'r') as file:
        html_content = file.read()

    # Build the table with player data
    table_html = '''
        <table>
            <tr>
                <th>DBU Name</th>
                <th>MobilePay Name</th>
                <th>Deposit</th>
                <th>Dept</th>
                <th>Balance</th>
            </tr>
    '''
    with open(player_data_path, 'r') as file:
        player_data = json.load(file)

    for player in player_data['payingPlayers']:
        table_html += f'''
            <tr>
                <td>{player['dbu_name']}</td>
                <td>{player['mobilepay_name']}</td>
                <td>{player['Deposit']}</td>
                <td>{player['Dept']}</td>
                <td>{player['balance']}</td>
            </tr>
        '''

    table_html += '''
        </table>
    '''

    # Append the table before the closing </body> tag
    updated_html_content = html_content.replace('</body>', table_html + '</body>')


    # Write the updated content back to the index.html file
    with open(html_file_path, 'w') as file:
        file.write(updated_html_content)

    print(f"Data appended successfully to {html_file_path}")