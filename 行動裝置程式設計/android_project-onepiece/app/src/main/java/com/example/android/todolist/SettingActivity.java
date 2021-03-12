package com.example.android.todolist;

import android.content.Intent;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v4.app.NavUtils;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.Switch;

import static com.example.android.todolist.MainActivity.flag;
import static com.example.android.todolist.MainActivity.mp;
import static com.example.android.todolist.MainActivity.musicOnSwitch;

public class SettingActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState)  {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.setting);
        Button remindQA;
        remindQA=(Button) findViewById(R.id.remindQA);
        remindQA.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startReminder();
            }
        });


        ActionBar actionBar = this.getSupportActionBar();
        // Set the action bar back button to look like an up button
        musicOnSwitch=(Switch) findViewById(R.id.musicOnSwitch);
        musicOnSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                switch (buttonView.getId()) {
                    case R.id.musicOnSwitch:
                        if (buttonView.isChecked()) {
                                mp.start();
                        } else {
                            mp.pause();
                            flag=false;
                        }
                }
            }
        });

        if (actionBar != null) {
            actionBar.setDisplayHomeAsUpEnabled(false);
        }
    }
    public void onPause(){
        super.onPause();
        if(!musicOnSwitch.isChecked()){
            mp.pause();
            flag=false;
        }
    }

    public void startReminder(){
        Intent intent=new Intent(SettingActivity.this,remind_quizActivity.class);
        startActivity(intent);
    }


//    @Override
//    public boolean onOptionsItemSelected(MenuItem item) {
//        int id = item.getItemId();
//        // When the home button is pressed, take the user back to the VisualizerActivity
//        if (id == android.R.id.home) {
//            NavUtils.navigateUpFromSameTask(this);
//
//        }
//        return super.onOptionsItemSelected(item);
//    }
}