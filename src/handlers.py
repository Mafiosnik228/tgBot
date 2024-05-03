import abc
import telegram as tg
import telegram.ext as tg_ext
import asyncpg 


async def create_connection():
    try:
        connection = await asyncpg.connect(user='', password='', database=' ', host='localhost')
        print("Успешное соединение с базой данных")
        return connection
    except Exception as e:
        print("Ошибка при соединении с базой данных:", e)
        return None

class baseHandler(abc.ABC):
    @abc.abstractclassmethod
    async def __call__(self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE) -> None:
        raise NotImplemented

class startHendler(baseHandler):
    async def __call__(self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        await update.message.reply_html(
            f"Hi {user.mention_html()}! Напиши задачу с командой /add и я запишу её а бд"
        )

class addHandler(baseHandler):
    async def __call__(self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE) -> None:
        try:
            task = " ".join(context.args)
            if not task:
                await update.message.reply_text('Пожалуйста, укажите задачу.')
            else:
                connection = await create_connection()
                await connection.execute('INSERT INTO tasks(task) VALUES($1)', task)
                await update.message.reply_text('Задача принята: ' + task)
                await connection.close()
        except Exception as e:
            await update.message.reply_text("Произошла ошибка при добавлении задачи. Пожалуйста, попробуйте снова.")

class tskHandler(baseHandler):
    async def __call__(self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE) -> None:
        try:
            con = await create_connection()
            records = await con.fetch('select * from tasks')
            message = "Данные из базы данных:"
            for record in records:
                message += f"{record}"
            await update.message.reply_text(message)

        except Exception as e:
            await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте снова.")

def setup_hendlers(aplication: tg_ext.Application) -> None:
    aplication.add_handler(tg_ext.CommandHandler('add', addHandler()))
    aplication.add_handler(tg_ext.CommandHandler('tsk', tskHandler()))
    aplication.add_handler(tg_ext.CommandHandler('start', startHendler()))