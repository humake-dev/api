namespace :poetry do
  desc "Install Python dependencies with poetry"
  task :install do
    on roles(:app) do
      within release_path do
        execute :poetry, "install --no-interaction --no-root"
      end
    end
  end
end