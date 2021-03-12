package com.example.android.todolist;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import com.example.android.todolist.QuizContract.*;

import java.util.ArrayList;


public class QuizDbHelper extends SQLiteOpenHelper {
    private static final String DATABASE_NAME = "MyAwesomeQuiz.db";
    private static final int DATABASE_VERSION = 1;

    private SQLiteDatabase db;

    public QuizDbHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        this.db = db;

        final String SQL_CREATE_QUESTIONS_TABLE = "CREATE TABLE " +
                QuestionsTable.TABLE_NAME + " ( " +
                QuestionsTable._ID + " INTEGER PRIMARY KEY AUTOINCREMENT, " +
                QuestionsTable.COLUMN_QUESTION + " TEXT, " +
                QuestionsTable.COLUMN_OPTION1 + " TEXT, " +
                QuestionsTable.COLUMN_OPTION2 + " TEXT, " +
                QuestionsTable.COLUMN_OPTION3 + " TEXT, " +
                QuestionsTable.COLUMN_ANSWER_NR + " INTEGER" +
                ")";

        db.execSQL(SQL_CREATE_QUESTIONS_TABLE);
        fillQuestionsTable();
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS " + QuestionsTable.TABLE_NAME);
        onCreate(db);
    }

    private void fillQuestionsTable() {
        Question q1 = new Question("空島人稱陸地上的人叫什麼?", "藍海人", "陸人", "天龍人", 1);
        addQuestion(q1);
        Question q2 = new Question("為什麼魯夫會變成橡皮人？", "a.卡普逼他吃橡膠果實", " b.生氣時不小心吃下香克斯放在一旁的橡膠果實", "c. 跟艾斯賭氣結果誤吃了橡膠果實", 2);
        addQuestion(q2);
        Question q3 = new Question("惡魔果實的剋星 下列何者為非?", "a. 海水", "b.海螻石", "c. 海草", 3);
        addQuestion(q3);
        Question q4 = new Question("是開始也是結束的地方是指?", "羅格鎮", "磁鼓島", "加亞島", 1);
        addQuestion(q4);
        Question q5 = new Question("偉大航道的起點?", "紅土大陸", "顛倒山", "魚人島", 2);
        addQuestion(q5);
        Question q6 = new Question("娜美最喜歡的水果?", "蘋果", "西瓜", "橘子", 3);
        addQuestion(q6);
    }

    private void addQuestion(Question question) {
        ContentValues cv = new ContentValues();
        cv.put(QuestionsTable.COLUMN_QUESTION, question.getQuestion());
        cv.put(QuestionsTable.COLUMN_OPTION1, question.getOption1());
        cv.put(QuestionsTable.COLUMN_OPTION2, question.getOption2());
        cv.put(QuestionsTable.COLUMN_OPTION3, question.getOption3());
        cv.put(QuestionsTable.COLUMN_ANSWER_NR, question.getAnswerNr());
        db.insert(QuestionsTable.TABLE_NAME, null, cv);
    }

    public ArrayList<Question> getAllQuestions() {
        ArrayList<Question> questionList = new ArrayList<>();
        db = getReadableDatabase();
        Cursor c = db.rawQuery("SELECT * FROM " + QuestionsTable.TABLE_NAME, null);

        if (c.moveToFirst()) {
            do {
                Question question = new Question();
                question.setQuestion(c.getString(c.getColumnIndex(QuestionsTable.COLUMN_QUESTION)));
                question.setOption1(c.getString(c.getColumnIndex(QuestionsTable.COLUMN_OPTION1)));
                question.setOption2(c.getString(c.getColumnIndex(QuestionsTable.COLUMN_OPTION2)));
                question.setOption3(c.getString(c.getColumnIndex(QuestionsTable.COLUMN_OPTION3)));
                question.setAnswerNr(c.getInt(c.getColumnIndex(QuestionsTable.COLUMN_ANSWER_NR)));
                questionList.add(question);
            } while (c.moveToNext());
        }

        c.close();
        return questionList;
    }
}
