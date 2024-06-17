import time
import detect
import repel
import lora_communication as lora

def main():
    try:
        lora.configure_LoRa()
    except Exception as e:
        print(f"LoRa configuration failed: {e}")
        return

    current_sound = None
    last_movement_time = time.time()

    while True:
        original_hash = lora.calculate_md5(repel.data_file_path)
        try:
            motion_detected = detect.detect_motion()
            if motion_detected:
                if current_sound is None:
                    current_sound = repel.play_random_sound()
                else:
                    if time.time() - last_movement_time >= 3:
                        print("1")
                        current_sound.stop()
                        repel.update_ranking(current_sound, increment=False)
                        current_sound = repel.play_random_sound()
                    else:
                        print("2")
                        current_sound.stop()
                        repel.update_ranking(current_sound, increment=True)
                    last_movement_time = time.time()
                
                new_hash = lora.calculate_md5(repel.data_file_path)
                updated = new_hash != original_hash
                if updated:
                    lora.lora_tx()
        except KeyboardInterrupt:
            print("랭킹:")
            ranking = repel.get_ranking()
            for index, (name, score) in enumerate(sorted(ranking.items(), key=lambda x: x[1], reverse=True), start=1):
                print(f"{index}: {name}: {score}")
            break

if __name__ == "__main__":
    main()
