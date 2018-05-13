def goal_generate_html(total_time, goal_id, goal_name, goal_type, days, hours,
                       minutes, start_time, end_time, all_categories,
                       goal_category):
    """Generates html for adding new goal."""

    html1 = "<li class=\"list-group-item\"> \
    <form> \
        <!-- Goal total time --> \
        <span> \
            {total_time} \
        </span> \
\
        <!-- Goal name --> \
        <span class=\"goal-input\"> \
            <span class=\"goal-{id}\"> \
                <input type=\"text\" value=\"{name}\" name=\"{id}\" \
                class=\"goal-input-field goal-name\"> \
            </span> \
        </span> \
 \
        <!-- Goal type --> \
        <span class=\"goal-type\"> \
            <span class=\"goal-{id}\"> \
 \
                <!-- Dropdown for seleting goal type --> \
                <span class=\"goal-type-dropdown goal-{id}\"> \
                    <select>".format(total_time=total_time, id=goal_id, name=goal_name)

    if goal_type == "at_least":
        html2 = "<option value=\"at_least\" selected>at least</option> \
                            <option value=\"at_most\">at most</option>"

    else:
        html2 = "<option value=\"at_least\">at least</option> \
                 <option value=\"at_most\" selected>at most</option> \
 \
                    </select> \
                </span> \
 \
            </span> \
        </span>"

    html3 = "<!-- Duration --> \
        <span class=\"goal-input duration\"> \
            <span class=\"goal-{id}\"> \
                <input class=\"goal-input-field duration days\" type=\"text\" \
                 value=\"{days}\" name=\"days-{id}\"> days \
 \
                <input class=\"goal-input-field duration hours\" type=\"text\"\
                 value=\"{hours}\" name=\"hours-{id}\"> hours \
 \
                <input class=\"goal-input-field duration minutes\" \
                type=\"text\" value=\"{minutes}\" name=\"minutes-{id}\"> \
                minutes \
            </span> \
        </span>".format(days=days, hours=hours, minutes=minutes,
                        id=goal_id)

    html4 = "<!-- Start and end dates --> \
        <span> \
            from \
            <span class=\"goal-start-time time-text\"> \
                {start_time} \
            </span> \
            <span class=\"goal-start-time time-input\"> \
                <input type=\"datetime-local\" name=\"startDate\" \
                class=\"date-time-picker\">  \
            </span> \
             \
            to \
            <span class=\"goal-end-time time-text\"> \
                {end_time} \
            </span> \
            <span class=\"goal-end-time time-input\"> \
                <input type=\"datetime-local\" name=\"endDate\" \
                class=\"date-time-picker\">  \
            </span> \
        </span>".format(start_time=start_time, end_time=end_time)

    html5 = "<!-- Categories --> \
        <span class=\"goal-title\"> \
            <span class=\"goal-{id}\"> \
\
                <!-- Dropdown for multiple selecting goals --> \
                <select multiple class=\"category-dropdown \
                goal-{id}\">".format(id=goal_id)

    html6 = ""

    for category in all_categories:
        if category in goal_category:
            html6 += "<option selected>{category_name}</option>".format(
                category_name=category.name)

        else:
            html6 += "<option>{category_name}</option>".format(
                category_name=category.name)

    html7 = "</select> \
                        </span> \
                    </span>\
            \
                    <!-- Save --> \
                    <span class=\"goal-edit-submit {id}Submit\"\
                     name=\"{id}\"> \
                        <span>save</span> \
                    </span> \
                </form> \
            </li>".format(id=goal_id)

    new_goal_html = html1 + html2 + html3 + html4 + html5 + html6 + html7

    return new_goal_html
