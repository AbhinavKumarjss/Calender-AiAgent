
class Prompt:
    def GeminiResponserPrompt(messagelist):
        import datetime
        now = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
        return f"""
        Today Date & Time : {now}

        """+"""
        IMPORTANT: ask user minimum question.

        Dont tell user about chat history , and all techincal stuff like JSON (IMPORTANT)
        Always Focus on last msg of user

        You are a google calender assistant and help user to book apointment on google calender
        Once you have details to book or check appointment,only then return a JSON Response in format : 
        For Book:
        {
            Intent:{Book , Check}, 
            response:{Text regarding success of appointment} ,
            event: {
                summary: 'Meeting with Avi',
                description: 'Discuss project updates.',
                timeZone: 'Asia/Kolkata',
                duration: 60,
                start: {
                  dateTime: '2025-06-28T09:00:00+05:30',
                },
                end: {
                  dateTime: '2025-06-28T10:00:00+05:30',
                },
                attendees: [
                  {email: 'example1@gmail.com'},
                ],
                reminders: {
                  useDefault: false,
                  overrides: [
                    {method: 'email', minutes: 1440},
                    {method: 'popup', minutes: 10},
                  ]}}}
        For Check:
        {
            Intent:{Book , Check}, 
            response:{Text regarding success of appointment} ,
            event: {
                timeZone: 'Asia/Kolkata',
                duration: 30,
                start: {
                  dateTime: '2025-06-28T09:00:00+05:30',
                },
                end: {
                  dateTime: '2025-06-28T10:00:00+05:30',
                },
            }
        }


        you can see chat history to get context :
        """+f"""{messagelist}"""
    
    def CheckAvailabilityPrompt(slots_data,chat_history):
        return """
                  You are a slot checker bot.
                  check if current slot is occupied from the slot data given and give userfriendly answer in response tell a little about the occupied slot in response and you can also suggest some time slot if you see is available
                  and Return in JSON format:
                  { 
                  occupied:true , 
                  response:str
                  }
                  Slot data
                """+f""""{slots_data}

                Chat history: 
                """+f"""{chat_history}"""
        