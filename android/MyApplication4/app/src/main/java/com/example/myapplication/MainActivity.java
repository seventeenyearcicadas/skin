package com.example.myapplication;


import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;
import org.xutils.common.Callback;
import org.xutils.http.RequestParams;
import org.xutils.x;

import java.io.File;
import java.util.Objects;

public class MainActivity extends AppCompatActivity {
    private Button btn_choose,btn_commit;
    private ImageView imageView;
    private TextView textView;
    Uri uri = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initView();
        btn_choose.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(Intent.ACTION_PICK, null);
                intent.setDataAndType(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, "image/*");
                startActivityForResult(intent, 2);


            }
        });
        btn_commit.setOnClickListener(new View.OnClickListener() {
            @RequiresApi(api = Build.VERSION_CODES.KITKAT)
            @Override
            public void onClick(View view) {
                textView.setText("waiting");
                RequestParams params = new RequestParams("http://192.168.1.171:5003/");
//                表单上传图片
                params.setMultipart(true);
//                实际图片路径
                String really_path = null;
                String[] proj = { MediaStore.Images.Media.DATA };
                Cursor cursor = getContentResolver().query(uri, proj, null, null, null);
                assert cursor != null;
                if(cursor.moveToFirst()){;
                    int column_index = cursor.getColumnIndexOrThrow(MediaStore.Images.Media.DATA);
                    really_path = cursor.getString(column_index);
                }
                assert really_path != null;
                Log.i("url:",really_path);
//                加载表单参数
                params.addBodyParameter("file", new File(really_path), null, "test.jpg");
                x.http().post(params, new Callback.CommonCallback<String>() {
                    @Override
                    public void onCancelled(CancelledException arg0) {

                    }

                    @Override
                    public void onError(Throwable ex, boolean isOnCallback) {
                        Toast.makeText(x.app(), ex.getMessage(), Toast.LENGTH_LONG).show();
                    }

                    // 不管成功或者失败最后都会回调该接口
                    @Override
                    public void onFinished() {
                    }

                    @Override
                    public void onSuccess(String msg) {
                        JSONObject jsonObject;
                        try {
                            textView.setText(msg);
                            jsonObject = new JSONObject(msg);
                            // TODO 业务处理
                        } catch (JSONException e) {
                            Log.e("evmsapp", e.getMessage());
                        }
                    }
                });
            }
        });
    }
    private void initView() {
        btn_choose = findViewById(R.id.choose);
        btn_commit = findViewById(R.id.commit);
        imageView = findViewById(R.id.imageview);
        textView = findViewById(R.id.txtOne);
    }

    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 2) {
            // 从相册返回的数据
            if (data != null) {
                // 得到图片的全路径
                uri = data.getData();
                imageView.setImageURI(uri);
            }
        }
    }


}