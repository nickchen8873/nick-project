package com.example.android.todolist;

import android.content.Intent;
import android.database.Cursor;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.ImageView;
import android.widget.TextView;

import com.example.android.todolist.data.TaskContract;

public class ItemActivity extends AppCompatActivity {
    TextView name1;
    //ImageView image;
    TextView desc;
    //TextView money;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_item);

        name1 = findViewById(R.id.TextName);
        desc = findViewById(R.id.TextDesc);
        //money = findViewById(R.id.TextMoney);

        String importName = MainActivity.important;


        System.out.println(TaskContract.TaskEntry.CONTENT_URI);
        Cursor cursor = getApplicationContext().getContentResolver().query(TaskContract.TaskEntry.CONTENT_URI,
                null,
                TaskContract.TaskEntry.COLUMN_DESCRIPTION + "=?",
                            new String[]{importName},
                null);

        //while (cursor.moveToNext()){
        cursor.moveToPosition(0);
            String name = cursor.getString(cursor.getColumnIndex(TaskContract.TaskEntry.COLUMN_DESCRIPTION));
            name1.setText(name);

            //String money1 = cursor.getString(cursor.getColumnIndex(TaskContract.TaskEntry.COLUMN_REWARD));
            //money.setText(money1);

            String introduce = cursor.getString(cursor.getColumnIndex(TaskContract.TaskEntry.COLUMN_INTRODUCE));
            desc.setText(introduce);
            cursor.moveToNext();

        //}
    }
}
