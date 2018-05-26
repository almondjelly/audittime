from model import Category

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
                    <select>".format(
                        total_time=total_time, id=goal_id, name=goal_name)

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
                 value=\"{days}\" name=\"days-{id}\">d \
 \
                <input class=\"goal-input-field duration hours\" type=\"text\"\
                 value=\"{hours}\" name=\"hours-{id}\">h \
 \
                <input class=\"goal-input-field duration minutes\" \
                type=\"text\" value=\"{minutes}\" name=\"minutes-{id}\" \
                >min \
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


def category_generate_html(category_id, category_name, all_goals,
                           category_goal):
    """Generates html for adding a new category."""

    html1 = "<tr class=\"tr-category\"> \
    <form class=\"form-category-id\"> \
        <!-- Category id --> \
        <input type=\"hidden\" class=\"input-category-id\" value=\"{category_id}\"> \
        <!-- Category name --> \
        <td class=\"td-category\"> \
            <input type=\"text\" value=\"{category_name}\" name=\"{category_id}\" class=\"td-input-category\"> \
        </td> \
        <!-- Category goals --> \
        <td class=\"td-category-goals\"> \
            <select multiple class=\"td-input-category-goals\">".format(
                category_name=category_name, category_id=category_id)

    html2 = ''.format()

    for goal in all_goals:
        if goal in category_goal:
            html2 += "<option selected>{}</option>".format(goal.name)
        else:
            html2 += "<option>{}</option>".format(goal.name)

    html3 = "</select> \
        </td> \
        <!-- Save --> \
        <td class=\"td-category-save\"> \
        <span class=\"span-category-save\"> \
            <button class=\"btn btn-primary\"><i class=\"material-icons\">save</i></button> \
        </span> \
        </td> \
        <!-- Archive --> \
        <td class=\"td-category-archive\"> \
        <span class=\"span-category-archive\"> \
            <button class=\"btn btn-primary btn-category-archive\"><i class=\"material-icons\">clear</i></button> \
        </span> \
        </td> \
    </form> \
    </tr>"

    new_category_html = html1 + html2 + html3

    return new_category_html


def task_generate_html():

    return new_task_html
"""<li> \
        <form> \
            <!-- Task --> \
            <span class=\"task-input\"> \
                <span class=\"event-{event_id}\"> \
                    <input type=\"text\" value=\"{task_name}\" name=\"{event_id2}\" class=\"input-field\"> \
                </span> \
            </span> \
\
            <!-- Category --> \
            <span class=\"category-title\"> \
                <span class=\"event-{event_id3}\"> \
                    {category_name} \
\
                    <!-- Dropdown for multiple selecting categories --> \
                    <div class=\"category-dropdown event-{event_id4}\"> \
                    <!-- ADD THE ACTUAL OPTIONS FOR PICKING CATEGORIES OR SOMETHING --> \
                        <ul> \
                            <li>asdf1</li> \
                            <li>asdf2</li> \
                            <li>asdf3</li> \
                        </ul> \
                    </div> \
                </span> \
            </span> \
\
            <!-- Duration --> \
            <span>{duration}</span> \
            <!-- Save --> \
            <span class=\"event-edit-submit {event_id5}Submit\">save</span> \
        </form> \
    </li>".format(event_id=event.event_id,
                  task_name=event.task.name,
                  event_id2=event.event_id,
                  event_id3=event.event_id,
                  category_name=event.task.category.name,
                  event_id4=event.event_id,
                  duration=event.duration(),
                  event_id5=event.event_id
                  )
"""